# Source coverage audit — 2026-07-22

The initial 16-repository sample was useful for testing the method, but it leaned toward developer tooling:

| Segment | Initial sources | Count |
|---|---|---:|
| Coding agents | Codex, Claude Code, OpenCode, Cline, OpenHands | 5 |
| Agent frameworks | browser-use, OpenAI Agents, AutoGen, LangGraph, Agno | 5 |
| Model/tool infrastructure | LiteLLM, MCP servers, FastMCP, Composio | 4 |
| Evaluation and observability | Langfuse, promptfoo | 2 |

This mix can make framework-internal pain look like universal user demand. It had no direct coverage of general assistant interfaces, local-first knowledge apps, or visual generation workflows.

## Added sources

| Repository | Added segment | Selection reason |
|---|---|---|
| `ollama/ollama` | Local model runtime | Widely used local-AI entry point |
| `open-webui/open-webui` | End-user assistant UI | User-facing interface across local and hosted models |
| `langgenius/dify` | Collaborative AI app builder | Covers non-code workflow and RAG application building |
| `Mintplex-Labs/anything-llm` | Local knowledge/RAG assistant | Covers document and local-first user workflows |
| `Comfy-Org/ComfyUI` | Visual generation | Adds a major non-text, node-based AI workflow audience |

All five were non-archived, updated within the previous 24 hours, and had more than 50,000 GitHub stars when reviewed. Stars are used only as a reach filter, not as evidence that a need exists.

The same 100-recent-issue window is retained for every repository. The expanded sample therefore contains 2,100 issues from 21 repositories without giving larger projects extra weight.

## Effect on the radar

| Need | Initial signal | Expanded signal | Interpretation |
|---|---:|---:|---|
| Verification and evidence | 64.2 | 59.8 | Still broad, but the initial developer-tool sample overstated it |
| Context and continuity | 57.7 | 57.8 | Stable and present in all five added segments |
| Cost and routing | 43.1 | 43.8 | Broadened enough to move from fourth to third |
| MCP interoperability | 45.0 | 39.3 | More concentrated in developer infrastructure than the initial rank suggested |

The durable cross-segment signal is context and continuity. That does not yet imply a standalone product: the reviewed issues include product-specific checkpoint and memory defects. The project gate remains four weekly snapshots plus another qualitative review before choosing an implementation experiment.
