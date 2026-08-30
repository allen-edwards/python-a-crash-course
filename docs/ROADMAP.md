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
- [ ] F11 Replace index.html's current generic tutor prompt (hardcoded, personalized to one student) with the full Professor Python teaching-method prompt (docs/PROFESSOR_PYTHON_PROMPT.md) — verified NOT done as of 2026-08-30 code review
- [ ] F16 Let the student state their name and learning preference (simple, editable field) and pass both into Professor Python's system prompt as context — no tracking or inference

### Phase 3 — Ideas / someday
- ~~Cinematic lesson playback with rendered video / generated backgrounds (F12)~~ — superseded by F14; see docs/ARCHITECTURE.md decision note. Not pursued: would require Node.js/FFmpeg (HyperFrames or similar), conflicting with the app's zero-dependency design.
- F10 Embedded lesson videos — folded into F14/lesson content work above
- Chapters 12+ (Pygame, data visualization, web apps) — idea stage, not yet scoped as requirements
- Dark/light theme toggle
- Mobile-friendly layout

## Next milestone
**v7.0 target:** One chapter has a working F14 faux-video lesson, end to end (script → animation → scrubbable playback), as a proof of concept before building the remaining 10 chapters' lessons.
