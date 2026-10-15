"""Rank manually researched affiliate niches from an evidence-backed CSV.

The tool intentionally does not scrape marketplaces or invent missing values.
All scores are user-entered ratings from 0 to 5. A total is shown only when
every factor has a score and the row includes its evidence and check date.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlsplit


WEIGHTS = {
    "demand": Decimal("0.25"),
    "product_signal": Decimal("0.20"),
    "commission": Decimal("0.20"),
    "demo": Decimal("0.20"),
    "competition": Decimal("0.10"),
    "policy_safety": Decimal("0.05"),
}
REQUIRED_COLUMNS = ("niche", *WEIGHTS, "evidence_urls", "checked_at")


class InputError(ValueError):
    """Raised when the CSV cannot be scored safely."""


def _score(value: str | None, field: str, row_number: int) -> Decimal | None:
    if value is None or not value.strip():
        return None
    try:
        score = Decimal(value.strip())
    except InvalidOperation as exc:
        raise InputError(f"Row {row_number}: {field} must be a number from 0 to 5.") from exc
    if not score.is_finite() or score < 0 or score > 5:
        raise InputError(f"Row {row_number}: {field} must be a number from 0 to 5.")
    return score


def score_row(row: dict[str, str], row_number: int = 2) -> dict[str, str]:
    """Return a normalized result row; incomplete evidence stays unranked."""
    niche = (row.get("niche") or "").strip()
    if not niche:
        raise InputError(f"Row {row_number}: niche is required.")

    scores = {name: _score(row.get(name), name, row_number) for name in WEIGHTS}
    missing = [name for name, value in scores.items() if value is None]
    evidence = (row.get("evidence_urls") or "").strip()
    checked_at = (row.get("checked_at") or "").strip()
    if evidence and not any(
        urlsplit(candidate.strip()).scheme in {"http", "https"}
        and bool(urlsplit(candidate.strip()).netloc)
        for candidate in evidence.split("|")
    ):
        raise InputError(f"Row {row_number}: evidence_urls must contain an http(s) URL.")
    if checked_at:
        try:
            date.fromisoformat(checked_at)
        except ValueError as exc:
            raise InputError(f"Row {row_number}: checked_at must use YYYY-MM-DD.") from exc

    if missing or not evidence or not checked_at:
        reasons = []
        if missing:
            reasons.append("missing: " + ", ".join(missing))
        if not evidence:
            reasons.append("missing evidence_urls")
        if not checked_at:
            reasons.append("missing checked_at")
        return {
            "niche": niche,
            "score": "",
            "status": "NEED_DATA",
            "missing": "; ".join(reasons),
            "evidence_urls": evidence,
            "checked_at": checked_at,
        }

    total = sum((scores[name] / Decimal("5") * weight * Decimal("100")
                 for name, weight in WEIGHTS.items()), Decimal("0"))
    return {
        "niche": niche,
        "score": f"{total.quantize(Decimal('0.1'))}",
        "status": "SCORED",
        "missing": "",
        "evidence_urls": evidence,
        "checked_at": checked_at,
    }


def rank_csv(input_path: Path, output_path: Path) -> list[dict[str, str]]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise InputError("Input CSV is empty.")
        absent = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if absent:
            raise InputError("Missing columns: " + ", ".join(absent))
        results = [score_row(row, index) for index, row in enumerate(reader, start=2)]

    results.sort(key=lambda item: (
        item["status"] != "SCORED",
        -Decimal(item["score"]) if item["score"] else Decimal("0"),
        item["niche"].casefold(),
    ))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=(
            "niche", "score", "status", "missing", "evidence_urls", "checked_at"
        ))
        writer.writeheader()
        writer.writerows(results)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Research CSV using the documented columns")
    parser.add_argument("--output", type=Path, default=Path("niche-rankings.csv"))
    args = parser.parse_args(argv)
    try:
        results = rank_csv(args.input, args.output)
    except (OSError, InputError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    scored = sum(result["status"] == "SCORED" for result in results)
    print(f"Saved {len(results)} niches to {args.output} ({scored} scored, {len(results) - scored} need data).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
