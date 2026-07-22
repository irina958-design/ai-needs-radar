# AI Needs Radar

An evidence-first radar for recurring needs across active AI repositories.

AI Needs Radar samples the 100 most recently updated issues from each selected project, classifies issue titles with public rules, and reports two things separately:

1. how broadly a pain appears across repositories;
2. how crowded the existing solution space already is.

That separation matters. A popular problem is not automatically a good new project. Session portability, observability, evals, routing, and proof-of-done are real pains, but each already has credible tools. The radar is designed to prevent us from shipping another generic clone.

## Latest snapshot

See [`data/latest.md`](data/latest.md) for the current evidence table and linked issue examples.

## Run it

Requirements: Python 3.11+ and a GitHub token with public repository read access.

```bash
export GITHUB_TOKEN=...
python radar.py
python -m unittest discover -s tests -v
```

On PowerShell:

```powershell
$env:GITHUB_TOKEN = gh auth token
python radar.py
python -m unittest discover -s tests -v
```

The weekly GitHub Action refreshes the public CSV snapshot and report.

## Files

- `sources.json` — repositories in the sample;
- `categories.json` — transparent patterns, labels, saturation scores, and known substitutes;
- `radar.py` — standard-library collector, classifier, and report generator;
- `data/` — current reproducible snapshot and compact dated summaries under `data/history/`;
- `tests/` — deterministic classification tests.

## Method and limits

- The unit is an issue title, not a user.
- Categories overlap by design.
- Equal 100-issue windows improve comparability but underrepresent high-volume repositories.
- GitHub issues contain maintainer work, feature requests, bugs, and self-promotion. Top signals require qualitative review.
- The current top-30 manual review is published in `data/reviewed_signals.csv`; it separates organic reports, promotion, and false positives.
- Stars measure ecosystem reach, not affected users.
- Saturation is a documented human judgment from 1 (few substitutes) to 5 (mature crowded category).

This project does not use an LLM to classify text. The first version stays cheap, inspectable, and reproducible.

## Roadmap

- Compare at least four weekly snapshots before choosing another product experiment.
- Accept repository and category nominations through issues.
- Add a lightweight static page only after the dataset proves useful.

## License

MIT
