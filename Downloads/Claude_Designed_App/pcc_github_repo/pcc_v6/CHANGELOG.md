# Changelog

All notable changes to **Python: A Crash Course — A Beginner's Journey** are documented here.

---

## [v6.0] — 2026-07-06 — Offline Support & Fixes

### Added
- `vendor/` folder with local copies of CodeMirror, Skulpt, and themes — sandbox and syntax highlighting now work fully offline (previously loaded from CDNs)
- `/vendor/<file>` route to serve the bundled libraries

### Fixed
- `/api/generate-script` route returning 404 — route was defined after `app.run()` and never registered. All routes now sit above the `__main__` block.
- Verified 2026-07-09: server started, all 6 routes tested — `/` 200, `/vendor/*` 200, `/api/progress` 200, `/api/run` executes code, `/api/tutor` and `/api/generate-script` respond (401 without an API key, as expected). No regressions.

### Changed
- Video-script system prompt reformatted (no behavior change)

---

## [v5.0] — 2026-07-04 — Major Feature Update

### Added
- New app title: *Python: A Crash Course — A Beginner's Journey*
- Credits section honouring Eric Matthes and both source books
- Collapsible sidebar (☰ toggle button)
- Side-by-side sandbox layout — code editor left, output right
- Syntax highlighting in the sandbox via CodeMirror (Dracula theme)
- "Try in sandbox" button pre-loads each chapter's example code
- Floating pop-out lesson panel — draggable and minimizable
- 📝 Generate Video Script button — creates original, copyright-safe YouTube scripts per chapter
- 🎬 Video placeholder slots in each lesson (ready for YouTube embeds)
- 4 new chapters: Ch 7 (While Loops), Ch 9 (Classes), Ch 10 (Files & Exceptions), Ch 11 (Testing)
- App icon (appIcon.png) bundled with the app
- Auto-creates desktop shortcut and app launcher entry on first run (Linux)
- Auto-creates Desktop launcher on macOS and Windows
- Windows launcher updated with new app name

### Changed
- App served as static file (bypasses Jinja2 template engine entirely — fixes JS syntax issues)
- All chapter data restructured with flat string properties (fixes object literal bug)

---

## [v4.0] — 2026-06-30 — Critical Bug Fix

### Fixed
- `/api/run` route returning 404 — route was defined after `app.run()` and never registered
- All routes now correctly defined before server starts

---

## [v3.0] — 2026-06-30 — Server-Side Python Runner

### Added
- `/api/run` endpoint — executes Python code server-side via subprocess
- Fallback to Skulpt (in-browser runner) if server is unreachable

### Fixed
- Run button producing no output in sandbox
- Skulpt CDN loading issues

---

## [v2.0] — 2026-06-29 — Full App Rewrite

### Added
- 7 chapters (Ch 1–6 + Ch 8) with full lessons, quizzes, and challenges
- XP system with chapter unlock progression
- Day streak tracker
- AI Tutor tab powered by Anthropic Claude API
- Quiz system with per-question feedback and XP rewards
- Progress dashboard
- Settings panel with API key management
- Persistent progress saved to progress.json via Flask

### Fixed
- Jinja2 template engine mangling JavaScript object literals
- Switched from render_template to send_file to serve HTML as static

---

## [v1.0] — 2026-06-29 — Initial Release

### Added
- Basic Flask server with progress save/load
- 3 chapters (Ch 1, 2, 3) with lessons and quizzes
- In-browser Python sandbox using Skulpt
- XP and streak tracking
- AI Tutor (basic version)
- Ubuntu virtual environment support to bypass externally-managed-environment error
- Desktop launcher (.desktop file) for Ubuntu
