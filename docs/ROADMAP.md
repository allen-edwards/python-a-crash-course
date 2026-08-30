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
- [ ] F15 Professor Python as an animated Lottie character (idle/thinking/wave), usable in the lesson player and as the static app icon
- [ ] F11 Professor Python as a persona-driven AI tutor (may reuse the F15 Lottie character as its visual presence; see PROFESSOR_PYTHON_PROMPT.md)

### Phase 3 — Ideas / someday
- ~~Cinematic lesson playback with rendered video / generated backgrounds (F12)~~ — superseded by F14; see docs/ARCHITECTURE.md decision note. Not pursued: would require Node.js/FFmpeg (HyperFrames or similar), conflicting with the app's zero-dependency design.
- F10 Embedded lesson videos — folded into F14/lesson content work above

## Next milestone
**v7.0 target:** One chapter has a working F14 faux-video lesson, end to end (script → animation → scrubbable playback), as a proof of concept before building the remaining 10 chapters' lessons.
