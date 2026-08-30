# Changelog

All notable changes to **Python: A Crash Course — A Beginner's Journey** are documented here.

---

## 2026-08-30 (session close) — F11 & F16 Verified Live; F17 Added; Voice Idea Parked
### Verified
- F11 (Professor Python prompt swap): confirmed via live tutor conversation — analogy-first explanations, predict-before-run questions, no unprompted name use, ambiguous-spelling handling all present and matching the prompt document. Marked Done.
- F16 (name/learning preference): confirmed via live tutor conversation with real Settings input. Name used naturally, not forced. Noted limitation: stated brevity preference ("short explanations") did not meaningfully shorten responses — logged as a known soft-signal limitation, not a bug, for future revisiting. Marked Done.

### Added
- F17: readability fix — default text sizing required repeated manual zooming; scoped fix is better default font/line-height plus a persistent font-size control.
- Roadmap note: new code examples appearing mid-conversation can be easy to miss — minor visual-distinction polish item, not urgent.
- Roadmap (parked, Phase 3): natural voice-to-text/TTS tutor interaction — explicitly tied to a possible future **hosted web version** of the app, since local voice models conflict with N7 and the offline/USB-portable design. Not scoped or committed.

---

## 2026-08-30 (absolute last) — Archived Historical CLAUDE.md
### Docs
- Archived the recovered 2026-07-06 CLAUDE.md as `docs/history/CLAUDE_2026-07-06.md`, unmodified except for a header note marking it historical and pointing to current docs. Kept for project history — not updated in place, since its value is showing design intent at that point in time.
- Note: no live/current CLAUDE.md exists at the repo root as of this pull. If Claude Code maintains one elsewhere for session context, it should be updated separately to reflect current decisions (F11 done, F16 added, fixed-personality rule) — that would be a distinct, current-state file, not this archived snapshot.

---

## 2026-08-30 (very last) — Reconciled with Original Project Notes (found on external drive, dated 2026-07-06)
### Docs
- Found and reviewed an earlier CLAUDE.md and PROFESSOR_PYTHON_PROMPT.md from before v6.0, recovered from the external drive.
- Confirmed and made explicit: F16 (name/learning preference) does not let students customize Professor Python's core personality or teaching method — that stays fixed and identical for every student, per the original 2026-07-06 design intent. F16 only adds context (name, stated preference), the same category as already knowing the current chapter.
- Corrected N4: the API key is stored client-side in browser localStorage (key: `pcc_key`), not just "not written to disk" as previously stated — confirmed against actual index.html code.
- Noted for the record: the original 2026-07-06 plan envisioned a much more ambitious "Cinematic Lesson Player" (Canvas-API generative art, Web Speech API narration, motion-graphics feel). F14 is a deliberate scope-down from that vision, not an oversight — documented so a future session doesn't mistake the simpler version for a forgotten original plan.

---

## 2026-08-30 (final) — Code Review Correction + New Feature (F16)
### Corrected
- Verified against actual code (index.html ~line 825): F11 is **not** done. The live tutor system prompt is generic and hardcoded to a specific student by name, with short/emoji-tuned style — it is not Professor Python's teaching-method prompt. Docs previously implied ambiguity here; now corrected with the exact line reference.

### Added
- **F16**: student-stated name and learning preference (e.g. "lots of examples," "step-by-step"), passed into Professor Python's system prompt as plain context. Deliberately scoped to stated preferences only — no behavior tracking, no inferred learning style, no psychological profiling. Rationale: anyone using this app has already chosen to put in the effort; this is about helping them succeed, not studying them.

---

## 2026-08-30 (later still) — Professor Python Scope Clarified
### Docs
- Confirmed docs/PROFESSOR_PYTHON_PROMPT.md (the full teaching-method system prompt) governs the **AI tutor chat only** (F6/F11) — not F14's faux-video lessons, which stay a non-interactive script → animation → playback pipeline.
- F6 relabeled: the existing tutor chat *is* Professor Python — he's the app's identity, not a separate planned feature. What's still Planned is wiring his actual system prompt in (tracked as F11, narrowed from "add a persona" to "apply this specific prompt").
- F15 (Lottie animation) clarified as supporting the tutor/app identity, not F14 lessons; personality traits (calm, patient, curious) should ground the animation's motion style.

---

## 2026-08-30 (later) — Documentation Cleanup
### Docs
- README.md: split Features into "Available now" vs "Coming soon" — previously implied F10 (video embeds) was ready when it's only a placeholder, and listed no planned features at all.
- README.md: removed its own separate, drifting roadmap list; it now points to docs/ROADMAP.md as the single source of truth.
- Recovered two orphaned ideas from the old README roadmap that weren't tracked anywhere else (dark/light theme toggle, mobile-friendly layout) and "Chapters 12+" — added to docs/ROADMAP.md's Phase 3 (someday) so they aren't lost.
- README.md: Project Structure diagram updated to include vendor/ and docs/, which existed in the repo but weren't listed.

---

## 2026-08-30 — Planning
### Docs
- Superseded F12 (rendered/cinematic lesson video) with **F14: in-app faux-video lesson player** — live browser animation (HTML/CSS/JS) inside a scrubbable player shell, instead of exporting real video files. Decision: HyperFrames (HTML-to-MP4 rendering) was evaluated and rejected for this use case since it requires Node.js/FFmpeg, which conflicts with the app's zero-install, USB-portable design.
- Added **F15: Professor Python as an animated Lottie character** (idle/thinking/wave), usable both as the static app icon and as an animated guide in the lesson player / AI tutor chat. Runs via the client-side `lottie-web` library — no new system dependency.
- Added non-functional requirement N7: no feature may require a runtime beyond a browser and Python.
- Added docs/ROADMAP.md (new file) — Phase 1 (done), Phase 2 (current focus: F13, F14, F15, F11), Phase 3 (someday/superseded items).
- Set next milestone (v7.0): one chapter's F14 lesson working end-to-end, as a proof of concept before building all 11.

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
