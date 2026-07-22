#!/usr/bin/env python3
"""Build a transparent issue-level needs radar from public GitHub repositories."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import urllib.request
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path


GRAPHQL_URL = "https://api.github.com/graphql"
QUERY = """
query($owner:String!, $name:String!, $limit:Int!) {
  repository(owner:$owner, name:$name) {
    nameWithOwner
    url
    stargazerCount
    pushedAt
    issues(first:$limit, orderBy:{field:UPDATED_AT, direction:DESC}) {
      nodes { number title state createdAt updatedAt url comments { totalCount } }
    }
  }
}
"""


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def graphql(token: str, variables: dict) -> dict:
    payload = json.dumps({"query": QUERY, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ai-needs-radar",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]["repository"]


def collect(sources: list[str], limit: int, token: str) -> tuple[list[dict], list[dict]]:
    repositories: list[dict] = []
    issues: list[dict] = []
    for full_name in sources:
        owner, name = full_name.split("/", 1)
        repo = graphql(token, {"owner": owner, "name": name, "limit": limit})
        repositories.append(
            {
                "repo": repo["nameWithOwner"],
                "stars": repo["stargazerCount"],
                "pushed_at": repo["pushedAt"],
                "url": repo["url"],
            }
        )
        for issue in repo["issues"]["nodes"]:
            issues.append(
                {
                    "repo": repo["nameWithOwner"],
                    "number": issue["number"],
                    "title": issue["title"],
                    "state": issue["state"].lower(),
                    "comments": issue["comments"]["totalCount"],
                    "created_at": issue["createdAt"],
                    "updated_at": issue["updatedAt"],
                    "url": issue["url"],
                }
            )
        print(f"{full_name}: {len(repo['issues']['nodes'])} issues")
    return repositories, issues


def classify(issues: list[dict], categories: list[dict]) -> tuple[list[dict], list[dict]]:
    compiled = {category["id"]: re.compile(category["pattern"], re.I) for category in categories}
    matches: list[dict] = []
    by_category: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for issue in issues:
        for category_id, pattern in compiled.items():
            if pattern.search(issue["title"]):
                matches.append({**issue, "category": category_id})
                by_category[category_id][issue["repo"]] += 1

    summaries: list[dict] = []
    total_repos = len({issue["repo"] for issue in issues})
    category_by_id = {category["id"]: category for category in categories}
    for category_id, per_repo in by_category.items():
        category = category_by_id[category_id]
        repos_with_match = len(per_repo)
        repos_with_3plus = sum(count >= 3 for count in per_repo.values())
        matched_issues = sum(per_repo.values())
        breadth = repos_with_match / total_repos if total_repos else 0
        saturation = int(category["saturation"])
        signal = round((breadth * 60) + (repos_with_3plus / total_repos * 25) + min(matched_issues, 100) / 10 - saturation * 8, 1)
        summaries.append(
            {
                "category": category_id,
                "label": category["label"],
                "matched_issues": matched_issues,
                "repos_with_match": repos_with_match,
                "repos_with_3plus": repos_with_3plus,
                "saturation_1_to_5": saturation,
                "priority_signal": signal,
                "substitutes": "; ".join(category.get("substitutes", [])),
            }
        )
    summaries.sort(key=lambda row: row["priority_signal"], reverse=True)
    return summaries, matches


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, date: str, repositories: list[dict], issues: list[dict], summaries: list[dict], matches: list[dict]) -> None:
    top_examples: dict[str, list[dict]] = defaultdict(list)
    for item in sorted(matches, key=lambda row: (row["comments"], row["updated_at"]), reverse=True):
        if len(top_examples[item["category"]]) < 3:
            top_examples[item["category"]].append(item)

    lines = [
        f"# AI needs radar — {date}",
        "",
        f"Snapshot: **{len(issues):,} recent issues** from **{len(repositories)} active AI repositories**.",
        "",
        "> This is a discovery signal, not a user census. Categories overlap; titles are classified with public regex rules; solution saturation is manually reviewed.",
        "",
        "## Signals",
        "",
        "| Rank | Need | Issues | Repos | 3+ matches | Saturation | Priority signal |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(summaries, 1):
        lines.append(
            f"| {rank} | {row['label']} | {row['matched_issues']} | {row['repos_with_match']} | {row['repos_with_3plus']} | {row['saturation_1_to_5']}/5 | {row['priority_signal']} |"
        )
    lines.extend(["", "## Evidence examples", ""])
    for row in summaries[:5]:
        lines.append(f"### {row['label']}")
        lines.append("")
        for issue in top_examples[row["category"]]:
            lines.append(f"- [{issue['repo']} #{issue['number']}: {issue['title']}]({issue['url']}) — {issue['comments']} comments")
        if row["substitutes"]:
            lines.append(f"- Existing substitutes: {row['substitutes']}")
        lines.append("")
    lines.extend(
        [
            "## How to read this",
            "",
            "- High breadth + low saturation is a candidate for qualitative research.",
            "- High breadth + high saturation means the pain is real, but another generic tool is probably redundant.",
            "- A project should not be started from this table alone; inspect issue bodies, authorship, substitutes, and a testable first use case.",
            "",
            "Generated by [`radar.py`](../radar.py).",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=Path("sources.json"))
    parser.add_argument("--categories", type=Path, default=Path("categories.json"))
    parser.add_argument("--output", type=Path, default=Path("data"))
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required (GitHub Actions provides it automatically).")

    args.output.mkdir(parents=True, exist_ok=True)
    date = datetime.now(UTC).date().isoformat()
    sources = load_json(args.sources)
    categories = load_json(args.categories)
    repositories, issues = collect(sources, args.limit, token)
    summaries, matches = classify(issues, categories)

    write_csv(args.output / "repositories.csv", repositories)
    write_csv(args.output / "issues.csv", issues)
    write_csv(args.output / "summary.csv", summaries)
    write_csv(args.output / "matches.csv", matches)
    write_report(args.output / "latest.md", date, repositories, issues, summaries, matches)
    (args.output / "metadata.json").write_text(
        json.dumps(
            {"generated_at": datetime.now(UTC).isoformat(), "repositories": len(repositories), "issues": len(issues)},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
