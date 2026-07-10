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
| F10 | The user can watch embedded lesson videos in each chapter | Nice | Placeholder slots ready; no videos yet |
| F11 | The user can talk to Professor Python, a persona-driven AI tutor | Nice | Planned (see PROFESSOR_PYTHON_PROMPT.md) |
| F12 | The user can watch cinematic lesson playback (generated backgrounds, animated code typing, narration) | Nice | Planned |
| F13 | The user can browse a Projects tab with hands-on practice projects | Nice | Planned |

## Non-functional requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| N1 | Runs on Windows, macOS, and Ubuntu with Python 3.8+ | Must | Done (launcher scripts for each OS) |
| N2 | Core features (lessons, sandbox, quizzes, progress) work without internet | Must | Done (v6.0 bundles editor/runner libraries locally) |
| N3 | Sandbox code executions time out after 10 seconds to prevent hangs | Must | Done |
| N4 | The user's API key is entered by the user and sent only to the Anthropic API | Must | Done (key travels browser → local server → Anthropic; never written to disk) |
| N5 | Progress data is stored in a human-readable local file (progress.json) | Nice | Done |
| N6 | App requires only one third-party dependency (Flask) | Nice | Done |

## Out of scope
- User accounts or cloud sync — the app is deliberately single-user and local.
- Bundling an API key — learners supply their own for AI features.
- Multiplayer or social features.

## Known constraints
- The sandbox executes arbitrary Python on the host machine via subprocess; this is acceptable for a single-user local app but means the app should never be exposed to a network (server binds to 127.0.0.1 only — see ARCHITECTURE.md).
