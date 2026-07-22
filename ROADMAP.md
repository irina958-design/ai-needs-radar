# Roadmap

AI Needs Radar follows evidence gates, not a feature calendar. The purpose of this roadmap is to decide **whether anything new should be built**, then keep the first experiment narrow enough to stop cheaply.

**Current phase:** evidence accumulation  
**Decision milestone:** 10 August 2026  
**Tracking issue:** [#9 — Four-week decision gate](https://github.com/irina958-design/ai-needs-radar/issues/9)

## Timeline

| Date | Checkpoint | Required output | Status |
|---|---|---|---|
| 22 Jul 2026 | Expanded baseline | 2,100 issues from 21 repositories | Complete |
| 27 Jul 2026 | Weekly snapshot 2 | Dated aggregate in `data/history/` | Scheduled |
| 3 Aug 2026 | Weekly snapshot 3 | Dated aggregate in `data/history/` | Scheduled |
| 10 Aug 2026 | Weekly snapshot 4 | Dated aggregate in `data/history/` | Scheduled |
| 10–12 Aug 2026 | Evidence review | Written go / no-go decision | Pending |
| 13–26 Aug 2026 | Narrow experiment | Only if every gate condition passes | Conditional |
| 27 Aug 2026 | Experiment review | Continue, change, or stop | Conditional |

The scheduled snapshots run automatically every Monday at 06:17 UTC.

## Phase 0 — Research foundation

**Status: complete**

- [x] Build a transparent issue collector and classifier.
- [x] Cover 21 repositories and 2,100 recent issues per snapshot.
- [x] Add user-facing, local-AI, RAG, and visual-generation sources.
- [x] Separate breadth from solution saturation.
- [x] Manually review 30 leading matches.
- [x] Correct OAuth and login false positives in permissions.
- [x] Store compact dated summaries.
- [x] Verify the weekly GitHub Action end to end.

## Phase 1 — Accumulate comparable evidence

**Status: now · 22 July–10 August**

The only required work in this phase is keeping the scheduled collection healthy.

### Exit criteria

- [ ] Four distinct dated summaries exist in `data/history/`.
- [ ] Every scheduled run completes successfully.
- [ ] The source list and category rules stay unchanged during the comparison window unless a data-quality defect requires a documented correction.

### Do not build yet

- GUI or dashboard;
- database or user accounts;
- plugin system or API;
- LLM classifier;
- a product based on the current leading category.

Changing the measurement system during the four-week window would make the snapshots harder to compare. A necessary correction must be recorded in the decision note.

## Phase 2 — Four-week decision gate

**Target: 10–12 August**

The review will:

1. compare rank, repository breadth, repeated breadth, and priority score across all four snapshots;
2. re-review the top 10 matches for the most stable cross-segment category;
3. inspect issue bodies and authorship for organic demand, promotion, and incidental matches;
4. re-check native features and existing substitutes;
5. publish a dated decision note under `data/decisions/`.

### Go conditions

Proceed to one experiment only if **all** conditions pass:

| Condition | Minimum evidence |
|---|---|
| Stable | The need ranks in the top three in at least 3 of 4 snapshots |
| Broad | It appears in at least 75% of sampled repositories in the final snapshot |
| Organic | At least 7 of the re-reviewed top 10 matches describe genuine user or maintainer pain |
| Underserved | No known substitute covers one specific workflow with comparable effort |
| Testable | That workflow can be tested with one experiment in seven development days or fewer |

If any condition fails, publish a **no-build** decision and keep collecting. A no-build result is a successful outcome of the radar.

## Phase 3 — One narrow experiment

**Target: 13–26 August · conditional**

The experiment must solve one workflow for one primary user. Its exact form is chosen at the gate; it is not predetermined to be a GUI, CLI, library, or service.

### Required scope

- one-sentence problem statement;
- one primary workflow;
- no account system, database, plugin architecture, or paid infrastructure unless the workflow cannot exist without it;
- five reproducible scenario tests;
- a short usage guide;
- a public feedback issue tied to the tested workflow.

### Experiment success criteria

- all five scenarios are reproducible and at least four complete successfully;
- at least three independent users confirm the same underlying problem from real workflows;
- at least two users attempt the solution more than once or integrate it into an existing workflow;
- no simpler native feature or existing tool provides the same result.

## Phase 4 — Continue, change, or stop

**Target: 27 August · conditional**

| Decision | Rule |
|---|---|
| Continue | Every experiment success criterion passes |
| Change scope | The problem is confirmed, but the proposed workflow or delivery form is wrong |
| Stop | Demand is weak, one-off, promotional, or already adequately served |

Stopping means preserving the evidence and lessons, closing the experiment, and returning to radar collection. It does not mean expanding the feature set to search for a use case.

## Later, only when justified

- Generate a trend chart after at least four comparable snapshots exist.
- Add repository and category nomination forms after external contributors begin proposing sources.
- Add a static public view after readers demonstrate repeated use of the Markdown and CSV outputs.
- Consider title-and-body classification only if manual reviews keep finding more than 30% false positives after rule tuning.

## Roadmap rules

1. Evidence gates features; dates do not force them.
2. One experiment at a time.
3. Prefer deletion and native platform features over new infrastructure.
4. Every new phase needs an observable success and stop condition.
5. Research data and negative decisions remain public.
