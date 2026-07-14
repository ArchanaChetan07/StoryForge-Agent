# StoryForge Research-to-Script Agent

### Plan â†’ search â†’ revise thin results â†’ brief â†’ HITL â†’ shoot-ready script.

[![GitHub](https://img.shields.io/badge/repo-StoryForge-Agent-181717?logo=github)](https://github.com/ArchanaChetan07/StoryForge-Agent)
[![Language](https://img.shields.io/badge/language-Python-3572A5)](https://github.com/ArchanaChetan07/StoryForge-Agent)
[![License](https://img.shields.io/badge/license-See%20repository-yellow)](https://github.com/ArchanaChetan07/StoryForge-Agent)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](https://github.com/ArchanaChetan07/StoryForge-Agent/actions)

---

## Overview

Creators need structured research briefs and scripts from live web sources with human approval before final generation.

Streamlit UI drives agent/loop with planner that searches (Tavily), revises once if thin, generates brief, then HITL-gated script using Google Generative AI; MCP server exposes tools; DEMO_MODE stubs when keys missing.

Agentic storytelling assistant with traces, HITL, and MCP surface.

This repository is maintained as **production-minded portfolio work**: clear architecture, automated checks where present, and metrics that are **traceable to committed artifacts** (never invented).

---

## Architecture

Topic query â†’ run_research_phase (plan/search/revise/brief) â†’ optional HITL approve â†’ run_script_phase â†’ display sources + script; MCP mirrors tools.

```mermaid
flowchart TB
  Q[Topic query] --> R[run_research_phase]
  R --> S[search_web via Tavily]
  S --> V{thin results?}
  V -->|yes once| RV[revise_query + re-search]
  V -->|no| B[generate_brief]
  RV --> B
  B --> H{HITL approve?}
  H -->|yes| SC[generate script]
  H -->|no| WAIT[wait]
  SC --> UI[Streamlit display]
```

```mermaid
sequenceDiagram
  participant U as User/Client
  participant S as Service/Pipeline
  participant E as Eval/Tools
  U->>S: request / job
  S->>E: execute
  E-->>S: results
  S-->>U: report / response
```

---

## Results & repository facts

> Only values found in code, configs, tests, or generated reports are listed. Absence of a clinical/ML accuracy number means it was **not** published in-repo.

| Metric | Value | Source |
|---|---|---|
| Tracked repository files | **22** | `git tree` |
| Python modules | **17** | `git tree *.py` |
| Tracked files | **22** | `git tree` |
| Python modules | **17** | `git tree` |
| Test-related paths | **3** | `git tree` |
| CI workflows | **Yes** | `.github/workflows` |
| Docker present | **No** | `repo root` |

```mermaid
%%{init: {'theme':'base'}}%%
pie showData title Language composition (bytes)
    "Python" : 100
```

---

## Key features

- Research phase: search â†’ observe â†’ revise if thin â†’ brief
- HITL approval before script generation
- Source cards in UI
- Demo mode stubs
- MCP server companion
- Tracing spans for debug

---

## Tech stack

| Layer | Technology |
|---|---|
| ui | Streamlit |
| llm | Google Generative AI |
| search | Tavily |
| mcp | MCP |
| ci | GitHub Actions |

---

## Skills demonstrated

Python · S · t · r · e · a · m · CI/CD · testing · automation

Keyword surface: **Python · Python · machine-learning · CI/CD · testing · API · Docker · automation · data-science · software-engineering · system-design · observability · LLM · cloud**

---

## Project structure

```text
StoryForge-Agent/
â”œâ”€â”€ app.py
â”œâ”€â”€ mcp_server.py
â”œâ”€â”€ agent/{loop,planner,tools,hitl,types}.py
â”œâ”€â”€ utils/{config,generator,search,styles,tracing}.py
â”œâ”€â”€ tests/
â”œâ”€â”€ requirements.txt
â””â”€â”€ .env.example
```

---

## Installation & usage

```bash
git clone https://github.com/ArchanaChetan07/StoryForge-Agent.git
cd StoryForge-Agent
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

## How it works

Entering a topic runs the research agent: search, optionally revise thin results (min sources/chars), synthesize a brief, then after approval generate a script. Missing API keys flip DEMO_MODE for stubbed search/generation.

---

## Future improvements

- Publish MIN_SOURCES/MIN_RAW_CHARS defaults in README
- Add eval set for brief/script quality

---

## License

See repository.

---

<p align="center">
  <b>StoryForge Research-to-Script Agent</b><br/>
  <a href="https://github.com/ArchanaChetan07/StoryForge-Agent">github.com/ArchanaChetan07/StoryForge-Agent</a>
</p>
