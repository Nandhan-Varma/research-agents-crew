# AI Research Crew

A multi-agent research assistant built with [crewAI](https://crewai.com). Given any topic, a crew of four specialized agents searches the web, extracts and organizes factual claims, writes a cited report, and cross-checks every claim against its source — producing a final, verified markdown report.

## How It Works

The crew runs a sequential pipeline where each task's structured output feeds the next:

```mermaid
flowchart LR
    A[Researcher<br/>web search + extraction] -->|ResearchFindings| B[Analyst<br/>claim extraction]
    B -->|AnalystFindings| C[Writer<br/>report drafting]
    C -->|ResearchReport| D[Verifier<br/>fact cross-check]
    D -->|VerifiedReport| E[output/research_report.md]
```

| Agent | Role | Tools |
|-------|------|-------|
| **Researcher** | Searches the web for recent developments on the topic; collects raw findings with source URLs and extracted page content | `TavilySearchTool`, `TavilyExtractorTool` |
| **Analyst** | Extracts discrete factual claims from raw findings, groups them into thematic categories, and explicitly flags contradictions | — |
| **Writer** | Turns structured claims into a report with executive summary, key findings (each with its citation), and future outlook | — |
| **Verifier** | Cross-checks every key finding against the Analyst's original fact list; flags untraceable claims instead of silently deleting them | — |

Every stage emits a typed [Pydantic](https://docs.pydantic.dev) model (`ResearchFindings` → `AnalystFindings` → `ResearchReport` → `VerifiedReport`, defined in `src/ai_research_crew/models.py`), so citations are carried through the pipeline structurally rather than by prompt alone.

## Installation

Requires Python >=3.10, <3.14 and [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
pip install uv        # if you don't have uv yet
crewai install        # lock and install dependencies
```

### Environment

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

## Usage

Run from the project root — you'll be prompted for a research topic:

```bash
crewai run
```

The final verified report is written to `output/research_report.md`, and each stage's structured output is saved alongside it:

```
output/
├── research.json          # Researcher — raw findings with URLs
├── analysis.json          # Analyst — extracted claims, categories, conflicts
├── research_report.json   # Writer — drafted report
├── complete_report.json   # Verifier — final verified report
└── research_report.md     # Rendered markdown report
```

## Project Structure

```
ai_research_crew/
├── src/ai_research_crew/
│   ├── config/
│   │   ├── agents.yaml    # Agent roles, goals, backstories, LLMs
│   │   └── tasks.yaml     # Task descriptions and expected outputs
│   ├── tools/              # Custom tools
│   ├── crew.py             # Crew assembly (agents, tasks, process)
│   ├── main.py             # Entry point (run, train, replay, test)
│   ├── models.py           # Pydantic output schemas
│   └── render.py           # VerifiedReport → markdown renderer
├── tests/
├── output/                 # Generated reports
└── pyproject.toml
```

## Customization

- `src/ai_research_crew/config/agents.yaml` — define or tune agents (role, goal, backstory, LLM)
- `src/ai_research_crew/config/tasks.yaml` — define or tune tasks
- `src/ai_research_crew/crew.py` — add tools, change the process, or rewire task context
- `src/ai_research_crew/models.py` — adjust the structured output schemas
- `src/ai_research_crew/main.py` — change inputs (topic, current year) or output handling

