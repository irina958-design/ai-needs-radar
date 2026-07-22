import unittest

from radar import classify


CATEGORIES = [
    {
        "id": "continuity",
        "label": "Continuity",
        "pattern": r"\b(?:session|resume|memory)\b",
        "saturation": 2,
        "substitutes": [],
    }
]


class ClassifyTests(unittest.TestCase):
    def test_counts_breadth_and_repeated_matches(self):
        issues = [
            {"repo": "a/one", "title": "Resume session", "comments": 1, "updated_at": "2026-01-01", "url": "u1"},
            {"repo": "a/one", "title": "Session memory lost", "comments": 2, "updated_at": "2026-01-02", "url": "u2"},
            {"repo": "a/one", "title": "Another session bug", "comments": 0, "updated_at": "2026-01-03", "url": "u3"},
            {"repo": "b/two", "title": "Resume history", "comments": 3, "updated_at": "2026-01-04", "url": "u4"},
            {"repo": "c/three", "title": "Unrelated", "comments": 0, "updated_at": "2026-01-05", "url": "u5"},
        ]

        summary, matches = classify(issues, CATEGORIES)

        self.assertEqual(len(matches), 4)
        self.assertEqual(summary[0]["matched_issues"], 4)
        self.assertEqual(summary[0]["repos_with_match"], 2)
        self.assertEqual(summary[0]["repos_with_3plus"], 1)

    def test_categories_can_overlap(self):
        categories = CATEGORIES + [
            {
                "id": "audit",
                "label": "Audit",
                "pattern": r"\b(?:memory|audit)\b",
                "saturation": 1,
                "substitutes": [],
            }
        ]
        issues = [{"repo": "a/one", "title": "Memory audit", "comments": 0, "updated_at": "2026-01-01", "url": "u"}]

        _, matches = classify(issues, categories)

        self.assertEqual({match["category"] for match in matches}, {"continuity", "audit"})


if __name__ == "__main__":
    unittest.main()
