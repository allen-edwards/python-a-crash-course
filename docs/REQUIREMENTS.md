# Requirements

## Purpose
Python: A Crash Course — A Beginner's Journey is a self-contained desktop learning app that teaches Python fundamentals through interactive lessons, a live code sandbox, quizzes with XP rewards, and an AI tutor. It runs entirely on the learner's own machine; only the AI features require internet access.

## Functional requirements
What the user can do. Status reflects the code as of 2026-07-09.

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| F1 | The user can read 11 interactive chapters covering Python fundamentals (Hello World through Testing) | Must | Done |
| F2 | The user can write and run real Python code in a sandbox with syntax highlighting | Must | Done |
| F3 | The user can take quizzes and earn XP; chapters unlock as XP grows | Must | Done |
| F4 | The user's progress (XP, streak, completed chapters, quiz scores) is saved between sessions | Must | Done |
| F5 | The user can maintain a day streak that tracks consecutive learning days | Must | Done |
| F6 | The user can chat with an AI tutor (Claude) after entering their own API key | Must | Done |
| F7 | The user can generate an original YouTube video script for any chapter | Must | Done (404 bug fixed in v6.0) |
| F8 | The user can pop out a floating, draggable lesson panel while coding | Nice | Done |
| F9 | The user can collapse the sidebar for more screen space | Nice | Done |
| F10 | The user can watch embedded lesson videos in each chapter | Nice | Superseded by F14 (see below) |
| F11 | The user can talk to Professor Python, a persona-driven AI tutor | Nice | Planned (see PROFESSOR_PYTHON_PROMPT.md) |
| F12 | ~~The user can watch cinematic lesson playback (generated backgrounds, animated code typing, narration)~~ | Nice | Superseded by F14 — see decision note below |
| F13 | The user can browse a Projects tab with hands-on practice projects | Nice | Planned |
| F14 | The user can watch an in-app "faux video" lesson for each chapter — animated code-typing synced to a scrubbable progress bar, played inside a styled player shell, entirely in the browser | Nice | Planned |
| F15 | The user sees Professor Python as an animated Lottie character (idle, thinking, wave) — usable as the static app icon and as an animated guide inside the lesson player and/or AI tutor chat | Nice | Planned |

### Decision note: F12 → F14
F12 originally implied rendering real video files (generated backgrounds, narration, exported clips). After discussion, the app doesn't need portable video files — lessons only need to play inside the app itself. F14 replaces that idea with a lighter approach: play the animation live in the browser (HTML/CSS/JS) inside a fake video-player shell, instead of rendering to MP4. This avoids adding Node.js/FFmpeg as dependencies and preserves the app's zero-install, USB-portable design. It also lets a learner pause and copy the code being "typed," which a real video could never offer. Trade-off: this lesson format only plays inside the app — it can't be exported or uploaded elsewhere (e.g. YouTube). That's an accepted trade-off, not a gap, since portability was never the goal.

## Non-functional requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| N1 | Runs on Windows, macOS, and Ubuntu with Python 3.8+ | Must | Done (launcher scripts for each OS) |
| N2 | Core features (lessons, sandbox, quizzes, progress) work without internet | Must | Done (v6.0 bundles editor/runner libraries locally) |
| N3 | Sandbox code executions time out after 10 seconds to prevent hangs | Must | Done |
| N4 | The user's API key is entered by the user and sent only to the Anthropic API | Must | Done (key travels browser → local server → Anthropic; never written to disk) |
| N5 | Progress data is stored in a human-readable local file (progress.json) | Nice | Done |
| N6 | App requires only one third-party dependency (Flask) | Nice | Done |
| N7 | No feature may require installing a runtime beyond a browser and Python — no Node.js, FFmpeg, or other system-level dependency | Must | Guiding constraint for F14/F15 |

## Out of scope
- User accounts or cloud sync — the app is deliberately single-user and local.
- Bundling an API key — learners supply their own for AI features.
- Multiplayer or social features.
- Exporting lessons as standalone video files (MP4, etc.) — see F12 → F14 decision note.

## Known constraints
- The sandbox executes arbitrary Python on the host machine via subprocess; this is acceptable for a single-user local app but means the app should never be exposed to a network (server binds to 127.0.0.1 only — see ARCHITECTURE.md).
- Lottie animations (F15) are an asset-creation task, not a coding task — they require an animation tool (e.g. Adobe After Effects + Bodymovin, or LottieFiles' editor) to produce the `.json` animation files before they can be wired into the app.
