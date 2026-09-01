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
- [x] F14 v1 — **complete, all 11 chapters** (2026-08-31). Toggleable Video/Text lesson panel; Video mode plays a silent code-typing animation (editor+terminal split) with play/pause and a click/drag-scrub progress bar. Every chapter (1–11) has a `CHAPTER_SCRIPTS` entry, each using a worked example distinct from that chapter's sandbox challenge.
- [ ] F15 Professor Python as an animated Lottie character (idle/thinking/wave), usable as the app icon and alongside the AI tutor chat — not used in F14 video lessons
- [x] F11 Wire the full Professor Python teaching-method prompt into the `/api/tutor` system prompt — Done, verified 2026-08-30
- [x] F16 Student-stated name and learning preference, passed to Professor Python as context — Done, verified 2026-08-30
- [x] F17 Readability pass — Done. Base text raised to 16px / 1.6 line-height; Settings A−/A/A+ text-size control scales lessons, quizzes, tutor chat, and the code editor and persists (`fontSizePreference`).
- [x] **Content-integrity rewrite (all 11 chapters)** — Done 2026-08-31. Not an original F-numbered feature; a substantive fix that came out of testing. An audit found every chapter's sandbox challenge shipped a complete working solution as starter code, and ~3/4 quiz questions per chapter were near-verbatim recall of the lesson text. Every chapter's `challengeCode` is now a comment-only scaffold (student writes the real code), and all quiz questions are scenario/comprehension checks grounded in that chapter's own lesson. Also added a "Practice Challenge Design" rule to `docs/PROFESSOR_PYTHON_PROMPT.md` so the live tutor doesn't hand out minimal-variation copy-the-shape challenges. Sequence: Ch 1 (rewritten, then scope-corrected), Ch 2–5, Ch 6–11.

### Phase 3 — Ideas / someday
- ~~Cinematic lesson playback with rendered video / generated backgrounds (F12)~~ — superseded by F14; see docs/ARCHITECTURE.md decision note. Not pursued: would require Node.js/FFmpeg (HyperFrames or similar), conflicting with the app's zero-dependency design.
- F10 Embedded lesson videos — folded into F14/lesson content work above
- Chapters 12+ (Pygame, data visualization, web apps) — idea stage, not yet scoped as requirements
- Dark/light theme toggle
- Mobile-friendly layout
- **Natural-sounding voice-to-text / text-to-speech tutor interaction** — explicitly parked, not rejected. A good local voice model or free natural-sounding TTS would conflict with N7 (no runtime beyond browser + Python) and the app's offline, zero-install, USB-portable design. This only makes sense as part of a **separate, hosted web version** of the app (an "extension" product, not the local app) — a server-hosted version could freely call a cloud TTS/voice API without those local constraints. Not scoped or committed to; noted here so the idea isn't lost.
- New example code blocks in the tutor chat can be easy to miss mid-conversation, especially in longer responses — worth a visual treatment (border/label) to distinguish a new example from a reference to earlier code. Minor polish, not urgent.

## Next milestone
**v7.0 target:** Chapter 1 has a working F14 panel end to end — the toggleable Video/Text lesson panel, accessible from anywhere including the sandbox, replacing the current text pop-out. Video mode: silent code-typing animation with captions, scrubbable progress bar. Text mode: readable script content. Simple reset-on-toggle (no position syncing yet — that's F14a, deferred). No audio yet (F14b, deferred — depends on Allen producing narration via Speechify). Proof of concept before building the remaining 10 chapters.
