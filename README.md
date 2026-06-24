# StoryForge

**Real-time research briefs and short-form video scripts, powered by Gemini AI and live web search.**

StoryForge takes any topic, fetches the latest web results via Tavily, and uses Google Gemini to produce a concise research brief and a ready-to-shoot 30-second script for YouTube Shorts or Instagram Reels.

---

## Features

- **Live web search** — Tavily pulls fresh results so your content is never stale
- **AI research brief** — Gemini synthesises sources into a sharp, 200-word summary
- **Video script generation** — one click turns the brief into a punchy short-form script
- **MCP server** — exposes `research_topic` and `create_video_script` as tools for Claude Desktop

---

## Quick start

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd storyforge-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and TAVILY_API_KEY

# 4. Run the Streamlit app
streamlit run app.py
```

---

## MCP Server (Claude Desktop integration)

```bash
# Development inspector
mcp dev mcp_server.py

# Install for Claude Desktop
mcp install mcp_server.py
```

### Available MCP tools

| Tool | Description |
|------|-------------|
| `research_topic(query)` | Searches the web and returns a research brief |
| `create_video_script(query)` | Researches a topic and returns a short-form video script |

---

## Project structure

```
storyforge-agent/
├── app.py              # Streamlit UI
├── mcp_server.py       # MCP tool server
├── utils/
│   ├── search.py       # Tavily search wrapper
│   ├── generator.py    # Gemini generation wrapper
│   └── styles.py       # UI CSS
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API key |
| `TAVILY_API_KEY` | Tavily search API key |

Get your keys at [aistudio.google.com](https://aistudio.google.com) and [tavily.com](https://tavily.com).

> **Security note:** Never commit your `.env` file. The `.gitignore` in this repo excludes it by default.
