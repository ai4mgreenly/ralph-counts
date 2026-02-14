# ralph-counts

Metrics dashboard for the Ralph pipeline. Visualizes task execution stats — cost, tokens, time, iterations, and lines changed — from a JSONL data file. A Python HTTP server with a self-contained SPA.

Philosophy: deliberately minimalist. Python standard library, no framework, single-page HTML UI.

## Architecture

Part of a multi-service system:

| Service | Language | Port | Purpose |
|---------|----------|------|---------|
| **ralph-plans** | Go + SQLite | 5001 | Goal storage and state machine |
| **ralph-shows** | Deno + Preact | 5000 | Web UI dashboard |
| **ralph-runs** | Ruby | 5002 | Orchestrator + agent loop |
| **ralph-logs** | Go | 5003 | Real-time log streaming |
| **ralph-counts** | Python | 5004 | This project — Metrics dashboard |

### How It Works

A Python HTTP server that serves a self-contained SPA and a `/api/stats` endpoint reading `~/.local/state/ralph/stats.jsonl`. The SPA auto-refreshes every 30 seconds. No auth — all services are localhost-only.

### Data

Reads `~/.local/state/ralph/stats.jsonl` — one JSON object per line with fields: goal_file, started_at, exit_reason, model, reasoning, iterations, assistant_messages, tool_uses, tokens (input/output/cache_read/cache_create), cost_usd, time_seconds (llm/tools/other/total).

### Source Layout

```
serve.py               # Entry point, HTTP server, /api/stats endpoint
index.html             # Self-contained SPA (Chart.js, dark theme)
favicon.ico            # Favicon
```

### Goal Scripts

Goal management scripts live in `scripts/goal-*/run` (Ruby, return JSON). Symlinked from `scripts/bin/` and available on PATH via `.envrc`.

| Script | Purpose |
|--------|---------|
| `goal-list` | List goals by status |
| `goal-get` | Get a single goal |
| `goal-create` | Create a new goal (draft) |
| `goal-queue` | Queue a draft goal |
| `goal-start` | Mark a goal as running |
| `goal-done` | Mark a goal as done |
| `goal-stuck` | Mark a goal as stuck |
| `goal-retry` | Retry a stuck goal |
| `goal-cancel` | Cancel a goal |
| `goal-comment` | Add a comment to a goal |
| `goal-comments` | List comments on a goal |

## Development

### Tech Stack

- **Python 3** standard library (`http.server`)
- **Chart.js** 4.4.7 via CDN
- Self-contained SPA with inline CSS/JS
- Inter + JetBrains Mono fonts via Google Fonts

### Commands

```sh
python3 serve.py       # Start the server
./launch.sh            # Same thing
```

### Version Control

This project uses **git**.

### Code Style

- Python standard library idioms, no dependencies
- Single Python file at project root
- Self-contained HTML SPA with inline CSS/JS
- Goal scripts are Ruby, return JSON: `{"ok": true/false, ...}`
- Minimalist — no abstractions for one-time operations

### Environment

Configured via `.envrc` (direnv). `PATH` includes `scripts/bin/` for direct script access. Services communicate via `RALPH_*_HOST/PORT` env vars.

## Directory Structure

```
ralph-counts/
├── serve.py                             # Entry point, HTTP server, /api/stats
├── index.html                           # Self-contained SPA (Chart.js)
├── favicon.ico                          # Favicon
├── launch.sh                            # Entry point: runs serve.py
├── scripts/
│   ├── bin/                             # Symlinks to goal scripts (on PATH)
│   └── goal-*/run                       # Goal state management scripts
├── .claude/
│   ├── library/                         # Skills (modular instruction sets)
│   └── skillsets/                       # Composite skill bundles
├── .envrc                               # direnv config
└── AGENTS.md                            # This file
```

## Skills

Skills are modular instruction sets in `.claude/library/<name>/SKILL.md`.

- **Load a skill**: `/load <name>` reads the skill into context
- **Load multiple**: `/load name1 name2`

### Skillsets

Composite bundles in `.claude/skillsets/<name>.json`:

```json
{
  "preload": ["skill-a"],
  "advertise": [{"skill": "skill-b", "description": "When to use"}]
}
```

- `preload` — loaded immediately when skillset is activated
- `advertise` — shown as available, loaded on demand with `/load`

Available skillsets:

- `meta` — For improving the .claude/ system (preloads: jj, pipeline, goal-authoring, align)

### For Ralph

When Ralph executes a goal in this repo, it receives only `AGENTS.md` as project context. This file is responsible for getting Ralph everything it needs.

## Goal Authoring

Goals are markdown files with required sections: `## Objective`, `## Reference`, `## Outcomes`, `## Acceptance`.

Key principles: specify WHAT not HOW, reference liberally, make discovery explicit, include measurable acceptance criteria, trust Ralph to iterate.

Full guide: `.claude/library/goal-authoring/SKILL.md`

### Goal Authoring for This Repo

When creating goals targeting this repository, use `--org ai4mgreenly --repo ralph-counts`.

## Common Tasks

**Modifying the dashboard:** Edit `index.html` (Chart.js SPA), restart `serve.py`.

**Changing the data source:** Update `STATS_PATH` in `serve.py`.

**Adding a goal command:** Create `scripts/<name>/run` (Ruby, returns JSON), symlink from `scripts/bin/<name>`.

**Adding a skill:** Create `.claude/library/<name>/SKILL.md` with YAML frontmatter (name, description). Add to relevant skillset JSON.
