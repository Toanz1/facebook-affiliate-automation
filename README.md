# Affiliate Niche Studio

Free affiliate content workflow for TikTok, Shopee Video, and Facebook. This repository currently contains a Google Sheets + GitHub Actions draft-generation pipeline; it is not yet a finished desktop app or an auto-publisher.

The product direction is a local-first Windows tool for evaluating affiliate niches, preparing product briefs and platform-specific content, exporting vertical videos, and tracking results from official reports.

See [docs/PRODUCT_PLAN.md](docs/PRODUCT_PLAN.md) for:

- Candidate micro-niches and the first test hypothesis
- MVP workflow and measurable 4-week validation
- Platform API boundaries and manual publishing steps
- Phased development scope and excluded automation

A first Python CLI now scores manually researched niches with a weighted, evidence-backed 0–100 score. Missing factors, evidence URLs, or check dates remain unranked.

Run it with Python 3:

```bash
python niche_scorer.py niche-candidates.csv --output niche-rankings.csv
python -m unittest discover -s tests -v
```

No income is guaranteed. Rankings must be based on user-provided or approved data with visible sources and dates.
