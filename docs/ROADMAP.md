# Roadmap

## Vision
A self-contained, offline-first Python learning app — lessons, sandbox, quizzes, and an optional AI tutor — that runs from a USB drive on any machine with zero installation beyond Python itself.

## Phases

### Phase 1 — Core (done)
- [x] F1 Interactive chapters
- [x] F2 Code sandbox
- [x] F3 Quizzes & XP
- [x] F4 Persistent progress
- [x] F5 Day streak
- [x] F6 AI tutor chat
- [x] F7 Video script generator
- [x] F8 Floating lesson panel
- [x] F9 Collapsible sidebar
- [x] Offline vendor libraries (v6.0)

### Phase 2 — Lesson experience (current focus)
- [ ] F13 Projects tab — hands-on practice projects per chapter
- [ ] F14 In-app faux-video lesson player — animated code-typing in a scrubbable player shell, browser-only, no video export
- [ ] Per-chapter lesson content built for the faux-video player (11 chapters, one lesson each) — first chapter is the proof of concept; the rest follow once the format is validated
- [ ] F15 Professor Python as an animated Lottie character (idle/thinking/wave), usable as the app icon and alongside the AI tutor chat — not used in F14 video lessons
- [x] F11 Wire the full Professor Python teaching-method prompt into the `/api/tutor` system prompt — Done, verified 2026-08-30
- [x] F16 Student-stated name and learning preference, passed to Professor Python as context — Done, verified 2026-08-30
- [ ] F17 Readability pass — default font size and line-height are too small for comfortable reading without zooming in/out repeatedly. Fix: better defaults, plus a persistent font-size control (e.g. in Settings) so the student sets it once. Not a full redesign — scoped to sizing/spacing only.

### Phase 3 — Ideas / someday
- ~~Cinematic lesson playback with rendered video / generated backgrounds (F12)~~ — superseded by F14; see docs/ARCHITECTURE.md decision note. Not pursued: would require Node.js/FFmpeg (HyperFrames or similar), conflicting with the app's zero-dependency design.
- F10 Embedded lesson videos — folded into F14/lesson content work above
- Chapters 12+ (Pygame, data visualization, web apps) — idea stage, not yet scoped as requirements
- Dark/light theme toggle
- Mobile-friendly layout
- **Natural-sounding voice-to-text / text-to-speech tutor interaction** — explicitly parked, not rejected. A good local voice model or free natural-sounding TTS would conflict with N7 (no runtime beyond browser + Python) and the app's offline, zero-install, USB-portable design. This only makes sense as part of a **separate, hosted web version** of the app (an "extension" product, not the local app) — a server-hosted version could freely call a cloud TTS/voice API without those local constraints. Not scoped or committed to; noted here so the idea isn't lost.
- New example code blocks in the tutor chat can be easy to miss mid-conversation, especially in longer responses — worth a visual treatment (border/label) to distinguish a new example from a reference to earlier code. Minor polish, not urgent.

## Next milestone
**v7.0 target:** One chapter has a working F14 faux-video lesson, end to end (script → animation → scrubbable playback), as a proof of concept before building the remaining 10 chapters' lessons.
