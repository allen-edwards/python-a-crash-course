# Requirements

## Purpose
Python: A Crash Course — A Beginner's Journey is a self-contained desktop learning app that teaches Python fundamentals through interactive lessons, a live code sandbox, quizzes with XP rewards, and an AI tutor. It runs entirely on the learner's own machine; only the AI features require internet access.

## Functional requirements
What the user can do. Status reflects the code as of 2026-08-30.

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| F1 | The user can read 11 interactive chapters covering Python fundamentals (Hello World through Testing) | Must | Done |
| F2 | The user can write and run real Python code in a sandbox with syntax highlighting | Must | Done |
| F3 | The user can take quizzes and earn XP; chapters unlock as XP grows | Must | Done |
| F4 | The user's progress (XP, streak, completed chapters, quiz scores) is saved between sessions | Must | Done |
| F5 | The user can maintain a day streak that tracks consecutive learning days | Must | Done |
| F6 | The user can chat with Professor Python — the app's AI tutor persona and identity, powered by Claude — after entering their own API key | Must | Done — the tutor chat is Professor Python; its system prompt is the full teaching-method prompt (see F11, verified 2026-08-30). |
| F7 | The user can generate an original YouTube video script for any chapter | Must | Done (404 bug fixed in v6.0) |
| F8 | The user can pop out a floating, draggable lesson panel while coding | Nice | Done |
| F9 | The user can collapse the sidebar for more screen space | Nice | Done |
| F10 | The user can watch embedded lesson videos in each chapter | Nice | Superseded by F14 (see below) |
| F11 | The `/api/tutor` system prompt uses the full Professor Python teaching-method prompt verbatim (see docs/PROFESSOR_PYTHON_PROMPT.md), replacing the old generic student-specific prompt | Must | Done — verified 2026-08-30 via live tutor test (analogy-first explanations, predict-before-run questions, no unprompted name use) |
| F16 | The student can tell the app their name and describe how they learn best in a simple, editable Settings field. Both are passed into Professor Python's system prompt as stated context — no inference, no tracking, no behavior analysis. | Nice | Done — verified 2026-08-30. Note: stated brevity preferences ("short explanations") are currently treated as a soft signal alongside Professor Python's own judgment, not strictly enforced — see decision note below. |
| F17 | Default font size/line-height are readable without the student needing to zoom in/out repeatedly; a persistent font-size control is available (e.g. in Settings) | Nice | Done — base text bumped to 16px with 1.6 line-height for prose; Settings has an A−/A/A+ text-size control that scales lessons, quizzes, tutor chat, and the CodeMirror editor via a `--fs-scale` CSS variable; choice saved as `fontSizePreference` in progress.json and applied on load. |
| F12 | ~~The user can watch cinematic lesson playback (generated backgrounds, animated code typing, narration)~~ | Nice | Superseded by F14 — see decision note below |
| F13 | The user can browse a Projects tab with hands-on practice projects | Nice | Planned |
| F14 | A single toggleable lesson panel, accessible from anywhere in the app (including the sandbox) — replaces the current text-based pop-out. Two modes: **Video** (code-typing animation + captions, scrubbable progress bar, no audio in v1) and **Text** (readable lesson content, as today). Both modes render from one shared script per chapter. | Nice | Planned — v1 in progress (v7.0 milestone: one chapter working end to end) |
| F14a | (Future, v1.1+) Position-aware mode toggling: Video→Text opens text near the video's current position; Text→Video starts slightly *before* the reading position (small rewind buffer) — intentionally asymmetric. Deferred until v1's core mechanism is proven. | Nice | Deferred (v1.1) |
| F14b | (Future) Video mode narration audio, produced by Allen via Speechify from the same per-chapter script used for F14. Deferred — content-production bottleneck, not a blocker for F14 v1. When added, playback should sync to the audio rather than an internal timer. | Nice | Deferred |
| F15 | Professor Python appears as an animated Lottie character (idle, thinking, wave) — reflecting his calm, patient, curious personality (see PROFESSOR_PYTHON_PROMPT.md) — usable as the static app icon and alongside the AI tutor chat. Not used in F14 video lessons. | Nice | Planned |

### Decision note: F14 — phased build, v1 vs. v1.1 vs. future audio
F14 was scoped in three deliberate phases to avoid stalling on the hardest parts before the core mechanism is even proven:
- **v1 (current target, v7.0 milestone):** the toggleable panel exists, replacing the current text pop-out; Video mode plays a silent code-typing animation with captions, driven by a shared per-chapter script; Text mode shows the same content as readable text; toggling between modes simply resets to the top (no position tracking yet). One chapter, built and verified, before doing all 11.
- **v1.1 (F14a, deferred):** position-aware toggling — video syncs text to roughly its current spot; text syncs video to slightly before the reading position (an intentional asymmetry, matching how people actually reorient when switching direction). Requires shared position/beat-tracking between modes that's easier to add once v1's foundation works than to get right on the first attempt.
- **Future audio (F14b, deferred):** real narration recorded via Speechify per chapter, from the same script. Deliberately not blocking v1 — audio production is real work on Allen's side, independent of the coding, and the silent animation already provides real teaching value on its own. When added, the animation's timing should already be structured as a timeline/beat sequence (not raw fixed CSS durations) specifically so audio can be synced to it later without reworking the mechanism.

### Decision note: F16 brevity preferences are a soft signal, not enforced
Live testing (2026-08-30) showed that a stated preference for "short explanations" did not meaningfully shorten Professor Python's responses — he remained thorough and well-structured (headers, multiple sections) even when brevity was requested. This is an accepted, known limitation for now, not a bug: the fix would require an explicit prompt rule prioritizing brevity over structure when a student states that preference. Not yet implemented — worth revisiting if it continues to feel long-winded in practice.

### Decision note: voice interaction — parked for a hosted version, not this app
A natural-sounding voice-to-text/text-to-speech tutor interaction was considered and explicitly parked, not rejected. A good local voice model or free natural TTS would violate N7 (no runtime beyond browser + Python) and the app's offline, zero-install, USB-portable design. This only makes sense for a **separate, hosted web version** of the app — a different product, not a feature of the local one — where a cloud voice API could be used freely without local constraints. See docs/ROADMAP.md Phase 3.


Anyone using this app has already chosen to learn and put in the effort — F16 exists to help them succeed, not to study them. The student states their name and learning preference directly (a simple field they fill in and can edit anytime); Professor Python just reads and respects it, the same way a human tutor would take a student at their word. There is no tracking of quiz performance, no inferring a "learning style" from behavior, and no psychological profiling. If this ever seems worth expanding, that expansion should be re-evaluated deliberately, not drifted into.

**Important distinction:** F16 does not let students customize or weaken Professor Python's personality or teaching method. His character — patient, Socratic, hints-before-answers — is fixed and identical for every student; no setting changes *how* he teaches. F16 only gives him two additional facts to work *with*, the same category as already knowing the student's current chapter: a name to use, and a stated preference to keep in mind while still teaching the same way. This was an explicit early design decision (recorded 2026-07-06, before today's session): the personality should not be tamperable by the user.

### Decision note: Professor Python's scope
Professor Python is the app's identity — its face and voice — not a single feature. His full teaching-method prompt (docs/PROFESSOR_PYTHON_PROMPT.md) governs the **AI tutor chat only** (F6/F11): Socratic pacing, hints before answers, predict-before-run questions, patient tone. It does **not** apply to F14 (faux-video lessons) — those are a straight script → animation → playback pipeline with no interactivity or pacing logic. The teaching *tone* may still inform how per-chapter lesson scripts are written, but the lesson player itself never needs to wait for a student's answer.
### Decision note: F12 → F14 → scope history
F12 originally implied rendering real video files (generated backgrounds, narration, exported clips). An earlier draft (recorded 2026-07-06, in a since-superseded planning file) described this even more ambitiously: Canvas-API generative art backgrounds, Web Speech API narration, and a full motion-graphics feel. After discussion in this session, the app doesn't need portable video files or that level of generative visual complexity — lessons only need to play inside the app itself, and the core teaching value is the code-typing animation, not generated art. F14 is a **deliberate scope-down** from that original, more ambitious vision — not an oversight. It replaces both ideas with a lighter approach: play the code-typing animation live in the browser (HTML/CSS/JS) inside a fake video-player shell, instead of rendering to MP4 or building a generative-art engine. This avoids adding Node.js/FFmpeg as dependencies and preserves the app's zero-install, USB-portable design. It also lets a learner pause and copy the code being "typed," which a real video could never offer. Trade-off: this lesson format only plays inside the app — it can't be exported or uploaded elsewhere (e.g. YouTube), and it won't have the generative-art motion-graphics polish originally envisioned. That's an accepted trade-off, not a gap, since portability and visual spectacle were never the actual goal — teaching clearly was. If the more ambitious version is wanted later, it should be a deliberate future decision (a new F-item), not a silent revival of the old plan.

## Non-functional requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| N1 | Runs on Windows, macOS, and Ubuntu with Python 3.8+ | Must | Done (launcher scripts for each OS) |
| N2 | Core features (lessons, sandbox, quizzes, progress) work without internet | Must | Done (v6.0 bundles editor/runner libraries locally) |
| N3 | Sandbox code executions time out after 10 seconds to prevent hangs | Must | Done |
| N4 | The user's API key is entered by the user and sent only to the Anthropic API | Must | Done (key is entered by the user, stored client-side in browser localStorage under `pcc_key`, and sent per-request; never written to the server's disk) |
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
