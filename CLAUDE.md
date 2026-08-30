# CLAUDE.md — Project Context for Claude Code

This file gives Claude Code full context about this project so it can
make informed changes without needing the full conversation history.
Read this file before making any changes to the codebase.

> This file is kept current. When it goes stale, archive the old version
> under `docs/history/CLAUDE_<date>.md` (header-flagged as historical,
> content unchanged) before overwriting this one — see
> `docs/history/CLAUDE_2026-07-06.md` for the pattern.

---

## Project Identity

**Name:** Python: A Crash Course — A Beginner's Journey
**Type:** Self-contained local web app for learning Python
**Author:** Allen Edwards
**GitHub:** https://github.com/allen-edwards/python-a-crash-course
**Local working folder:** `~/projects/python-a-crash-course` — this is the
one true working copy. Other folders (Downloads, old zip extracts, etc.)
may contain stale copies — always confirm `git log --oneline -1` matches
the latest known commit before trusting a folder.
**Current version:** v6 (post-v6.0 doc/feature updates through 2026-08-30)

---

## What this app is

An interactive Python learning app that runs locally via Flask and opens
in the browser. It includes:
- 11 structured lessons based on original content
- Live Python sandbox (runs real Python via Flask subprocess)
- Quizzes with XP rewards and chapter unlock progression
- Day streak tracker
- **Professor Python** — the app's AI tutor identity and voice, powered by
  the Anthropic Claude API, using a full teaching-method system prompt
  (see `docs/PROFESSOR_PYTHON_PROMPT.md`)
- Video script generator for YouTube content
- Floating draggable pop-out lesson panel
- Collapsible sidebar
- Syntax highlighted code editor (CodeMirror + Dracula theme)
- Persistent progress saved to progress.json
- Student-stated name and learning preference (optional, Settings)
- Font-size toggle (Small/Medium/Large) for readability

---

## File Structure

```
python-a-crash-course/
├── app.py                  ← Flask server — ALL routes defined here
├── index.html              ← Complete app UI (single file, no templates)
├── appIcon.png             ← App icon (snake student at desk, yellow bg)
├── START_MAC_LINUX.sh      ← Launcher — creates venv, installs Flask, auto-creates desktop shortcut
├── START_WINDOWS.bat       ← Windows launcher
├── progress.json           ← User progress (auto-created, not tracked in git)
├── .venv/                  ← Virtual environment (auto-created, not tracked)
├── vendor/                 ← ALL JS/CSS libraries bundled locally (fully offline)
│   ├── skulpt.min.js       ← In-browser Python fallback
│   ├── skulpt-stdlib.js
│   ├── codemirror.min.js   ← Code editor
│   ├── codemirror.min.css
│   ├── dracula.min.css     ← Editor theme
│   └── python.min.js       ← Python syntax highlighting
└── docs/
    ├── REQUIREMENTS.md         ← Full feature list (F1–F17+), status, decision notes
    ├── ARCHITECTURE.md         ← How it's built, key decisions, planned-feature designs
    ├── ROADMAP.md              ← Phases, current focus, someday ideas
    ├── PROFESSOR_PYTHON_PROMPT.md  ← The tutor's full personality/teaching-method prompt (verbatim, do not summarize)
    └── history/
        └── CLAUDE_2026-07-06.md   ← Archived earlier version of this file, historical only
```

---

## Critical Architecture Rules

1. **app.py** — All Flask routes MUST be defined BEFORE `app.run()`.
   `app.run()` is always the very last thing in the file. This has caused
   404 bugs twice before (v4.0: `/api/run`; v6.0: `/api/generate-script`)
   — never append routes after app.run().

2. **index.html** — Served as a static file via `send_file()`, NOT as a
   Jinja2 template. Do NOT use `render_template()`. Jinja2 was breaking
   JavaScript object literals with curly braces.

3. **vendor/ folder** — All JS/CSS libraries load from vendor/ locally.
   The app must work completely offline. Never switch back to CDN links.
   The only external calls are to Anthropic's API (tutor + script generator).

4. **No new runtime dependency beyond a browser and Python** (N7 in
   REQUIREMENTS.md). No Node.js, no FFmpeg, no system-level installs for
   any feature. Before adding any dependency, check whether a
   browser-native (HTML/CSS/JS) approach covers the need first. This is
   why F14 (see below) is a live-animation player, not a video renderer.

5. **JavaScript** — Written in plain ES6 vanilla JS (no frameworks).
   No backtick template literals in CHAPTERS data objects — use regular
   string concatenation. This caused a major bug previously.

6. **Python runner** — Code runs via `/api/run` which uses
   `subprocess.run([sys.executable, ...])`. Runs real Python on the
   user's machine, not in-browser. Server binds to 127.0.0.1 only —
   keep it that way, since this route executes arbitrary code.

7. **API key handling** — User provides their own key, entered in
   Settings, stored client-side in browser `localStorage` (key: `pcc_key`),
   sent per-request. Never stored server-side or written to disk.

---

## Flask Routes (app.py)

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Serves index.html |
| `/vendor/<filename>` | GET | Serves local JS/CSS libraries |
| `/api/progress` | GET | Load saved progress |
| `/api/progress` | POST | Save progress |
| `/api/run` | POST | Execute Python code (subprocess) |
| `/api/tutor` | POST | Professor Python (Anthropic API) — system prompt sent from index.html |
| `/api/generate-script` | POST | Video script generator (Anthropic API) |

---

## API Details

**Model:** `claude-sonnet-4-6`
**Tutor timeout:** 30 seconds
**Script generator timeout:** 120 seconds (generates 8-12 min scripts)
**API key:** User provides their own, stored in browser localStorage
             (`pcc_key`), sent with each request in the `apiKey` field

---

## Professor Python — IMPORTANT

Professor Python is the app's identity, not a single feature. His full
teaching-method prompt lives in `docs/PROFESSOR_PYTHON_PROMPT.md` and is
wired verbatim into `index.html`'s `var sys` string (as of commit
`1299fc5`). Do not summarize, shorten, or paraphrase that prompt when
working with it — copy it verbatim.

**His core personality and teaching method are fixed and must not be made
user-configurable.** Every student gets the identical teaching approach
(patient, Socratic, hints before answers, predict-before-run questions).
This was an explicit, deliberate design decision — do not add settings
that let a student weaken or change *how* he teaches.

What students CAN provide (F16, done) is **additional context**, not
personality control:
- Their name (Settings → "About You")
- A stated learning preference (free text, e.g. "short explanations with
  examples") — used as a soft signal Professor Python considers, not a
  strict rule. (Known limitation: stated brevity preferences don't
  currently shorten his responses much — see decision note in
  REQUIREMENTS.md if revisiting this.)

Both fields are optional, editable anytime, stored in `progress.json`,
and only included in the tutor's system prompt when non-empty (never
send a line like "The student's name is ." with an empty value).

**Scope boundary:** Professor Python's prompt governs the AI tutor chat
only (F6/F11). It does NOT apply to F14 (faux-video lessons) — that's a
non-interactive script → animation → playback pipeline with no pacing
logic. Lesson script tone may still echo his teaching style, but the
player itself never waits for a student answer.

---

## Chapters (11 total)

| ID | Title | XP to unlock | XP reward |
|----|-------|-------------|-----------|
| 0 | Ch 1 — Hello World | 0 | 15 |
| 1 | Ch 2 — Variables | 10 | 15 |
| 2 | Ch 3 — Lists | 20 | 20 |
| 3 | Ch 4 — Loops | 50 | 20 |
| 4 | Ch 5 — if Statements | 90 | 20 |
| 5 | Ch 6 — Dictionaries | 130 | 25 |
| 6 | Ch 7 — While Loops | 180 | 25 |
| 7 | Ch 8 — Functions | 230 | 30 |
| 8 | Ch 9 — Classes | 290 | 35 |
| 9 | Ch 10 — Files & Exceptions | 360 | 35 |
| 10 | Ch 11 — Testing | 430 | 40 |

---

## UI Structure (index.html)

```
App layout (CSS Grid):
├── Topbar (full width) — title, XP bar, streak counter
├── Sidebar (collapsible) — chapter nav, progress, settings links
└── Main content area
    ├── Chapter view (default)
    │   ├── Tab: Lesson — HTML lesson content (F14 faux-video player: planned, not yet built)
    │   ├── Tab: Sandbox — CodeMirror editor (left) + output (right)
    │   ├── Tab: Quiz — 4 questions per chapter
    │   └── Tab: Professor Python — chat interface (renamed from "AI Tutor" in commit 1299fc5)
    ├── Progress view — XP stats + chapter progress bars
    └── Settings view — API key input, About You (name/learning pref), text-size toggle, credits

Floating elements:
├── Pop-out panel — draggable, minimizable lesson reference
└── Script modal — displays generated video script
```

---

## Planned Features — see docs/ROADMAP.md and docs/REQUIREMENTS.md for full detail

Quick summary, current priority order (Phase 2, roadmap):

### 1. F13 — Projects Tab
Bite-sized coding projects inspired by *The Big Book of Small Python
Projects*, appearing after core chapters.

### 2. F14 — In-app "Faux Video" Lesson Player (NEXT MILESTONE, v7.0)
**Important scope note:** an earlier draft (2026-07-06, archived in
`docs/history/`) envisioned a much more ambitious "Cinematic Lesson
Player" — Canvas API generative art, Web Speech API narration,
motion-graphics feel. That was deliberately scoped down in this session.
F14 as currently defined is simpler:
- Live browser animation (HTML/CSS/JS), NOT a rendered video file —
  no Node.js, no FFmpeg (violates N7).
- A styled player-shell UI (dark frame, play/pause, scrubbable progress
  bar) containing code that appears to type itself, matching the
  chapter's script (from the existing script generator).
- Progress bar syncs to an `<audio>` element (if narration is ever added)
  or an internal clock; scrubbing jumps the animation to that point.
- Student can pause and copy the code being "typed" — impossible with a
  real video file.
- v7.0 target: ONE chapter working end-to-end as proof of concept before
  building all 11.
- Does NOT use Professor Python's interactive/Socratic prompt — see
  scope boundary above.
- Does NOT use HyperFrames or any HTML-to-video renderer — evaluated and
  rejected for requiring Node.js/FFmpeg.

### 3. F15 — Professor Python as an animated Lottie character
JSON-based vector animation (`lottie-web`, no new system dependency) for
idle/thinking/wave states. Supports the AI tutor chat and app branding —
NOT used in F14 video lessons. Personality should ground the animation
style: calm, patient, curious — not high-energy mascot motion. Creating
the `.json` asset itself needs an external animation tool (After Effects
+ Bodymovin, or LottieFiles' editor) — not something written in code.

### Done (2026-08-30)
- F11 — Professor Python's real prompt wired into `/api/tutor`'s system
  prompt (was previously a generic, student-specific placeholder)
- F16 — name/learning-preference fields
- F17 — readability/font-size fix + toggle

### Someday / parked (see ROADMAP.md Phase 3 for full list)
- Chapters 12+ (Pygame, data viz, web apps) — idea stage
- Dark/light theme toggle
- Mobile-friendly layout
- Natural voice-to-text/TTS tutor interaction — parked for a possible
  future **hosted web version** of the app (different product, not this
  local one — local voice models would violate N7)

---

## Inspiration & Credits

This app was inspired by two books by Eric Matthes (No Starch Press):
- Python Crash Course
- The Big Book of Small Python Projects

All lesson content is original — nothing is copied from the books.
The credits are displayed in the Settings view of the app.

---

## Known History & Fixed Bugs

- **Jinja2 conflict** — Switched from render_template to send_file to
  prevent Flask mangling JavaScript object literals
- **Route after app.run()** — Happened twice: `/api/run` (v4.0) and
  `/api/generate-script` (v6.0). Always define routes before app.run().
- **CDN dependency** — All libraries moved to vendor/ after an internet
  outage broke the app. Never use CDN links.
- **venv on Ubuntu 24** — Ubuntu blocks system pip. Launcher creates a
  local .venv and uses VENV_PYTHON directly to avoid this.
- **Timeout** — Script generator needs 120s timeout (not 30s) due to
  4000 token response size.
- **Stale-code-in-doc-merge risk** — A "docs update" zip can sometimes
  contain an older copy of `index.html`/`app.py` alongside genuinely
  newer docs (happened 2026-08-30). Always diff a merge zip's code files
  against the current repo before applying — if the zip's code is older,
  apply the docs only and flag the mismatch rather than reverting working
  code.

---

## Git & GitHub

```bash
# Standard update workflow
cd ~/projects/python-a-crash-course
git status
git add .
git commit -m "description of change"
git push

# Credentials stored via:
git config --global credential.helper store
```

Remote: https://github.com/allen-edwards/python-a-crash-course.git
Branch: main

**Port note:** the dev server runs on port 5757. If it's already in use
(e.g. an old instance still running from earlier testing), `pkill -f
app.py` before starting a fresh one — this has caused confusion before
where testing happened against a stale running instance instead of
current code.

---

## User Preferences

- Allen prefers changes explained before implemented
- One command at a time in terminal instructions
- Downloadable files preferred over terminal commands when possible
- Progress.json and .venv should never be committed to git
- The app should always work fully offline except for AI features
- Allen is not a professional developer — keep explanations plain,
  avoid assuming prior programming/terminal experience
