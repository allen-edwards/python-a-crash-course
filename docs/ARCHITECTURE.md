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
| Vendor libs | Local CodeMirror so the app works offline | vendor/, served via /vendor/ route |
| Launchers | One-click start, venv setup, desktop shortcuts | START_MAC_LINUX.sh, START_WINDOWS.bat |

## Technology choices

| Choice | Why (one line) |
|--------|----------------|
| Flask | Minimal server; the app needs only 5 routes |
| Single index.html served via send_file | Bypasses Jinja2, which mangled JS object literals (see v2.0/v5.0 changelog) |
| subprocess for the sandbox | Runs real Python (not a browser approximation) with a 10-second timeout |
| urllib (stdlib) for the AI proxy | Avoids adding a requests dependency; keeps requirements.txt to Flask only |
| progress.json flat file | Single-user app; a database would be overkill |

## F14 — In-app lesson panel (Video/Text toggle) — v1 + audio (F14b) shipped, all 11 chapters

**Decision:** one panel, accessible from anywhere in the app (including mid-sandbox), replacing the old text-based pop-out. It has two modes the student can toggle between, both rendering from the same underlying per-chapter script:

- **Video mode:** a styled player-shell `<div>` (dark frame, play/pause, scrubbable progress bar) where code appears to type itself, paced against the script, with on-screen captions and real narration audio (F14b). No video encoding, no Node.js, no FFmpeg — pure HTML/CSS/JS, same as the rest of the app.
- **Text mode:** the same lesson content shown as plain readable text — this is what the old pop-out always did, and it still works standalone.

Because there's no real video file, switching modes is just swapping what's rendered inside the same `<div>` from the same source script — not two separate systems to maintain.

**Build is phased:**

1. **v1 — DONE, all 11 chapters (2026-08-31):** panel + toggle exist; Video mode is silent (captions only), timing driven by an internal clock structured as a **timeline of beats** (not raw fixed CSS animation durations) so audio can be added later without reworking the mechanism; Text mode shows the script as formatted text; toggling between modes simply resets to the top — no position syncing yet. Originally scoped as "one chapter as proof of concept," then extended to cover all 11 chapters in the same session once the mechanism was validated. Each chapter's video example is deliberately distinct from that chapter's sandbox challenge (see the content-integrity rewrite note below), so the video teaches the concept without accidentally giving away the challenge's answer.
2. **v1.1 (deferred, F14a):** position-aware toggling. Video→Text opens text near the video's current beat. Text→Video starts slightly *before* the student's reading position (a small rewind buffer) — this asymmetry is intentional, not a bug: switching *to* video usually means "I want to see this in action," which reads better starting just before the moment in question, not exactly at it. Requires a shared position/beat index between both modes — deliberately deferred until v1's core timing mechanism was proven, since retrofitting shared position state is easier than designing it correctly before anything works.
3. **Audio (F14b, DONE 2026-09-13):** narration recorded via Speechify per chapter (plain Text-to-Speech, verbatim single voice - not the "Podcast"/"Lecture" feature, which rewrites the text and generates multiple voices; that version is kept separately as a possible future companion-podcast idea, see ROADMAP.md), from the same script that drives the animation. Served via a new `/audio/<filename>` Flask route mirroring the existing `/vendor/<filename>` pattern. **Audio is now the actual timing source, not the internal clock**: as anticipated when v1 was built, the beat-timeline structure meant this was a swap of the time source feeding the existing render loop (`lpRenderAt`), not a rebuild of the animation logic. Two implementation details worth recording:
   - **Proportional beat rescaling.** Real recorded speech doesn't match the original silent-era time estimates (`getBeatDuration`) beat-for-beat - confirmed in practice (Chapter 1's real audio is 31.7s vs. a 42.3s silent estimate). Rather than hand-tuning per-beat timing for all 11 chapters, each beat's estimated duration is rescaled proportionally against the real `audio.duration` once its metadata loads, so a beat that was (say) 15% of the estimated runtime becomes 15% of the real audio's runtime. Good enough for v1; not frame-perfect beat-to-beat, but doesn't require manual tuning per chapter.
   - **In-beat typing speed stays at its original rate.** The code/run beats' character-by-character typing animation is timed in raw ms-per-character (`typeSpeedMs`), independent of the beat's own (now-rescaled) duration - the render function converts the rescaled "local" time back to raw-equivalent time specifically for that calculation, so typing doesn't finish early (or crawl) just because its containing beat got stretched or compressed to match real speech.
   - **Falls back cleanly** to the original silent/estimate-based playback if a chapter's audio fails to load (missing file, decode error, etc.) - verified by temporarily removing a chapter's audio file and confirming Video mode still works exactly as it did before F14b.

This whole approach was evaluated against HyperFrames (an open-source HTML-to-MP4 renderer used by AI coding agents) and deliberately rejected: HyperFrames is the right tool when a portable video *file* is the goal (e.g. for YouTube), but it requires Node.js 22+ and FFmpeg as local dependencies, which conflicts with N7 (no runtime beyond browser + Python) and the app's USB-portable design. Since lessons only ever need to play inside the app itself, live animation is strictly simpler and avoids the dependency entirely — and it lets a learner pause and copy the code being "typed," which a real video file never could.

## Content-integrity rewrite (all 11 chapters, 2026-08-31)

Not an F-numbered feature — a substantive fix that came out of testing F14, kept here since it's a real architectural/content-design decision worth recording. An audit found every chapter's sandbox `challengeCode` shipped a complete working solution (student only swapped placeholder text), and most quiz questions were near-verbatim lesson recall with implausible distractors. Fixed by rewriting all 11 chapters' challenges (comment-only scaffolding now) and quizzes (genuine comprehension checks, grounded only in that chapter's own taught content). A related addition — a "Practice Challenge Design" section in `docs/PROFESSOR_PYTHON_PROMPT.md` — extends the same discipline to the *live* AI tutor's on-the-fly challenges. See `docs/REQUIREMENTS.md` for the full decision note and `docs/PROFESSOR_PYTHON_PROMPT.md` for the added prompt section.

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
1. User clicks Run; browser POSTs `{code, simulatedInput}` to `/api/run` - `simulatedInput` comes from a small textarea in the sandbox UI, labeled for one line per `input()` call.
2. Flask executes the code with `python -c <code>` in a subprocess, capturing stdout/stderr, 10 s timeout.
3. **Simulated stdin for `input()` (added 2026-09-13, Ch7 fix):** `simulatedInput` is passed as `subprocess.run(..., input=simulated_text)` - the standard technique for feeding a one-shot, non-interactive subprocess's stdin from a string. Before this, `/api/run` never set `stdin` at all, so a subprocess whose code called `input()` inherited the Flask server's own stdin and hung until the 10 s timeout killed it - `input()` was untestable in the sandbox. A trailing newline is appended if missing, so the last `input()` call still gets one, matching a real terminal.
   - A blank `simulatedInput` is a no-op for code that never calls `input()` - stdin is simply never read, so this isn't a behavior change for the common case.
   - Because `subprocess.run(input=...)` writes the given text and then closes stdin, a script that calls `input()` more times than lines were provided fails **fast** with a clear `EOFError: EOF when reading a line` traceback, rather than hanging for the full timeout - a better outcome than originally anticipated when this was scoped, not just an acceptable v1 limitation.
   - The timeout error message itself was also improved to suggest checking for enough simulated input lines, as a defensive fallback for the genuine hang case (e.g. an unrelated infinite loop) where stdin isn't the cause.
4. JSON `{output, error}` returns to the browser and renders in the output box.
5. If the server is unreachable, `runCode()`'s `catch` block shows a plain error message ("Could not run code. Is the app server still running?"). **This doc previously claimed a Skulpt (in-browser Python) fallback existed here - it never did**, and the dead Skulpt vendor files/script tags were removed 2026-09-13 once confirmed genuinely unused. See the Key decisions log entry below for the full reasoning.

**Design constraint for future projects (F13 and beyond):** the sandbox executes code in one batch - `subprocess.run()`, captured output, optional pre-supplied simulated `input()` lines (see point 3 above). There is no live-refreshing terminal, no real-time key-press detection, and no continuous animation loop. This rules out real-time games (arrow-key movement, screen-clearing animations, anything requiring a live frame loop) as future mini-project or capstone candidates - that would need a genuinely different execution architecture, not a feature added on top of this one. It fully supports **turn-based interaction**: print something, `input()` a response, react, loop - which covers a wide range of genuinely fun projects (guessing games, text adventures, quizzes, simple board games represented as text) without needing any architecture change at all.

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
- 2026-09-13: **Skulpt fallback (2026-06-30 entry above) removed entirely - `skulpt.min.js`/`skulpt-stdlib.js` deleted, script tags removed.** It was built during early development when local server setup was occasionally unreliable; the app is now mature and stable enough that "the page loaded but the server has since vanished underneath it" isn't a reachable scenario - the app IS the server, so if it were down, the page wouldn't have loaded at all. Confirmed genuinely dead first (no code path referenced it) before removing. Building a real fallback instead was considered and rejected: Skulpt runs Python entirely differently (in-browser, no real subprocess or file I/O), so the input() support just built for the real sandbox (Ch7 Part 2, same day) would need solving a second time for a failure mode that can't really occur here - not worth the weight for this app's offline-portable, "lighter is better" identity.
