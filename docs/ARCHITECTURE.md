# Architecture

## Overview
The app is a single-page web application served by a tiny local Flask server. All UI, lesson content, and app logic live in one HTML file; the Python server exists to serve that file, persist progress, execute sandbox code, and proxy AI requests to the Anthropic API so the browser never has to deal with CORS.

## Components

```
                         ┌──────────────────────────────┐
   Browser (index.html)  │  Flask server (app.py :5757) │
 ┌─────────────────────┐ │                              │
 │ Lessons / Quizzes   │ │  GET  /               ──────────> serves index.html
 │ CodeMirror sandbox  ├───> POST /api/run       ──────────> subprocess (python -c)
 │ XP / streak logic   │ │  GET/POST /api/progress ────────> progress.json
 │ AI Tutor chat       ├───> POST /api/tutor     ──┐       │
 │ Script generator    ├───> POST /api/generate-script ─┤  │
 └─────────────────────┘ └────────────────────────│─────┘
                                                  ▼
                                       Anthropic API (claude-sonnet-4-6)
```

| Component | Responsibility | Key files |
|-----------|---------------|-----------|
| Frontend SPA | All UI, lesson content, quiz logic, XP/streak rules, CodeMirror editor | index.html (~84 KB, self-contained) |
| Flask server | Static serving, progress persistence, code execution, AI proxy | app.py |
| Progress store | Saves XP, streak, completed chapters, quiz scores | progress.json (created at runtime) |
| Vendor libs | Local CodeMirror + Skulpt so the app works offline | vendor/, served via /vendor/ route |
| Launchers | One-click start, venv setup, desktop shortcuts | START_MAC_LINUX.sh, START_WINDOWS.bat |

## Technology choices

| Choice | Why (one line) |
|--------|----------------|
| Flask | Minimal server; the app needs only 5 routes |
| Single index.html served via send_file | Bypasses Jinja2, which mangled JS object literals (see v2.0/v5.0 changelog) |
| subprocess for the sandbox | Runs real Python (not a browser approximation) with a 10-second timeout |
| urllib (stdlib) for the AI proxy | Avoids adding a requests dependency; keeps requirements.txt to Flask only |
| progress.json flat file | Single-user app; a database would be overkill |

## Data flow: running sandbox code
1. User clicks Run; browser POSTs the code to `/api/run`.
2. Flask executes it with `python -c <code>` in a subprocess, capturing stdout/stderr, 10 s timeout.
3. JSON `{output, error}` returns to the browser and renders in the output box.
4. If the server is unreachable, the frontend falls back to Skulpt (in-browser Python).

## Key rules for future changes
- **All routes must be defined above the `if __name__ == "__main__":` block.** Code below `app.run()` never executes while the server runs. This has caused two 404 bugs already (v4.0: /api/run, v6.0: /api/generate-script).
- The server binds to 127.0.0.1 only. Keep it that way — `/api/run` executes arbitrary code and must never be reachable from the network.
- API keys arrive per-request from the browser and are forwarded, never stored.

## Key decisions log
- 2026-06-29: send_file over render_template (Jinja2 conflicts with inline JS).
- 2026-06-30: server-side runner added; Skulpt kept as offline fallback.
- 2026-07-09: route-ordering rule documented after second 404-after-app.run() bug.
