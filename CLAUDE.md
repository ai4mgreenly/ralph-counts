# ralph-counts

Dashboard for visualizing Ralph task execution stats.

## Run

```
python3 serve.py
```

Opens at http://localhost:1982

## Data

Reads `~/.local/state/ralph/stats.jsonl` — one JSON object per line with fields: goal_file, started_at, exit_reason, model, reasoning, iterations, assistant_messages, tool_uses, tokens (input/output/cache_read/cache_create), cost_usd, time_seconds (llm/tools/other/total).

## Architecture

- `index.html` — self-contained SPA (Chart.js from CDN, Inter + JetBrains Mono fonts)
- `serve.py` — minimal Python HTTP server, serves index.html + `/api/stats` endpoint that reads the JSONL file

Auto-refreshes every 30 seconds. Re-reads file on browser refresh.

## Skills

Skills are modular instruction sets stored in `.claude/library/<name>/SKILL.md`.

- **Load a skill**: `/load <name>` reads the skill into context
- **Load multiple**: `/load name1 name2` loads several at once

## Skillsets

Skillsets are composite bundles of skills defined in `.claude/skillsets/<name>.json`.

- **Load a skillset**: `/skillset <name>` loads all preloaded skills and advertises on-demand ones
- **Skillset format**: JSON with `preload` (loaded immediately) and `advertise` (available via `/load`)

### Available skillsets

- `meta` - For improving the .claude/ system (jj)
