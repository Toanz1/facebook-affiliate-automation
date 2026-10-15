import unittest

from niche_scorer import InputError, score_row


class NicheScorerTests(unittest.TestCase):
    def row(self, **overrides):
        values = {
            "niche": "Tiện ích phòng trọ nhỏ",
            "demand": "4",
            "product_signal": "3",
            "commission": "2",
            "demo": "5",
            "competition": "3",
            "policy_safety": "5",
            "evidence_urls": "https://example.com/source",
            "checked_at": "2026-10-15",
        }
        values.update(overrides)
        return values

    def test_scores_complete_source_backed_row(self):
        result = score_row(self.row())
        self.assertEqual(result["status"], "SCORED")
        self.assertEqual(result["score"], "71.0")

    def test_missing_value_is_not_treated_as_zero(self):
        result = score_row(self.row(commission=""))
        self.assertEqual(result["status"], "NEED_DATA")
        self.assertEqual(result["score"], "")
        self.assertIn("commission", result["missing"])

    def test_missing_evidence_withholds_total(self):
        result = score_row(self.row(evidence_urls=""))
        self.assertEqual(result["status"], "NEED_DATA")
        self.assertIn("evidence_urls", result["missing"])

    def test_score_outside_range_is_rejected(self):
        with self.assertRaises(InputError):
            score_row(self.row(demand="5.1"))

    def test_invalid_evidence_url_is_rejected(self):
        with self.assertRaises(InputError):
            score_row(self.row(evidence_urls="not-a-url"))

    def test_invalid_check_date_is_rejected(self):
        with self.assertRaises(InputError):
            score_row(self.row(checked_at="yesterday"))

    def test_blank_niche_is_rejected(self):
        with self.assertRaises(InputError):
            score_row(self.row(niche=" "))


if __name__ == "__main__":
    unittest.main()
