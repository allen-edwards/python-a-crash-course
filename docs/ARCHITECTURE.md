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

## Planned: F14 — In-app faux-video lesson player

**Decision:** lessons play as live browser animation, not as rendered video files. No video encoding library, no Node.js, no FFmpeg — everything runs in the same HTML/CSS/JS the rest of the app already uses.

How it works, conceptually:
- A "player shell" — a styled `<div>` that looks like a video player (dark frame, play/pause button, scrubbable progress bar).
- Inside it, the actual "video" is a CSS/JS-driven animation: code appears to type itself, matching the chapter's script.
- An `<audio>` element (if narration is added later) or synced captions plays alongside; the progress bar tracks `audio.currentTime` (or an internal clock if there's no audio) so scrubbing jumps the animation to the right point.
- Because the "video" is just live code, a learner can pause and copy the code being typed — not possible with a real video file.

This was evaluated against HyperFrames (an open-source HTML-to-MP4 renderer used by AI coding agents) and deliberately rejected for this use case: HyperFrames is the right tool when a portable video *file* is the goal (e.g. for YouTube), but it requires Node.js 22+ and FFmpeg as local dependencies, which conflicts with N7 (no runtime beyond browser + Python) and the app's USB-portable design. Since this app's lessons only ever need to play inside the app itself, the live-animation approach is strictly simpler and avoids the new dependencies entirely.

## Planned: F15 — Professor Python as an animated Lottie character

**Decision:** use Lottie (JSON-based vector animations) for an animated Professor Python character, rendered via the `lottie-web` JavaScript library. This supports the **AI tutor chat and app identity** — it is not used in F14's video lessons (see decision note below).

Why Lottie fits this project specifically:
- Lottie files are JSON — tiny, resolution-independent, no video codec required.
- `lottie-web` runs entirely client-side in the browser; no new system dependency (fits N7).
- Animations are controllable from JS — play/pause/loop/jump-to-frame — so Professor Python can react to app state (idle loop, "thinking" while the AI tutor responds, a wave when a lesson starts).

Professor Python's personality (docs/PROFESSOR_PYTHON_PROMPT.md) should ground the animation style: calm, patient, curious, warm — not high-energy mascot motion. A gentle head-tilt for "thinking," a relaxed idle loop, a warm wave — not bouncing or exaggerated gestures.

Note: creating the `.json` Lottie animation itself is an asset-creation task (needs an animation tool such as After Effects + Bodymovin, or LottieFiles' web editor) — it is not something written in Python or JS from scratch. The static app icon (`appIcon.png`) is unaffected and can continue to use the same Professor Python artwork as a still image.

### Decision note: Professor Python's scope across features
Professor Python is the app's overall identity, not a single feature. His full teaching-method prompt governs the **AI tutor chat only** (F6/F11) — Socratic pacing, hints before answers, patient tone. F14 (faux-video lessons) is a separate, non-interactive pipeline (script → animation → playback) and does not use the tutor prompt or require Professor Python's animated presence, though lesson scripts may still be written in a tone consistent with his teaching style.

## Data flow: running sandbox code
1. User clicks Run; browser POSTs the code to `/api/run`.
2. Flask executes it with `python -c <code>` in a subprocess, capturing stdout/stderr, 10 s timeout.
3. JSON `{output, error}` returns to the browser and renders in the output box.
4. If the server is unreachable, the frontend falls back to Skulpt (in-browser Python).

## Key rules for future changes
- **All routes must be defined above the `if __name__ == "__main__":` block.** Code below `app.run()` never executes while the server runs. This has caused two 404 bugs already (v4.0: /api/run, v6.0: /api/generate-script).
- The server binds to 127.0.0.1 only. Keep it that way — `/api/run` executes arbitrary code and must never be reachable from the network.
- API keys arrive per-request from the browser and are forwarded, never stored.
- No new feature may require installing a runtime beyond a browser and Python (see N7). Before adding any dependency, check whether a browser-native (HTML/CSS/JS) approach covers the need first.

## Key decisions log
- 2026-06-29: send_file over render_template (Jinja2 conflicts with inline JS).
- 2026-06-30: server-side runner added; Skulpt kept as offline fallback.
- 2026-07-09: route-ordering rule documented after second 404-after-app.run() bug.
- 2026-08-30: F12 (cinematic/rendered lesson video) superseded by F14 (in-app faux-video player) — HyperFrames-style MP4 rendering rejected in favor of live browser animation, to preserve zero-install/USB-portable design (N7). F15 (Lottie-animated Professor Python) added as a compatible, dependency-free way to add an animated mascot.
