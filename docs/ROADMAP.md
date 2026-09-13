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
- [ ] F15 Professor Python as an animated Lottie character (idle/thinking/wave), usable as the app icon and alongside the AI tutor chat — not used in F14 video lessons. Pending: confirm Allen's LottieFiles account access/tier.
- [x] **Bug: "Mark complete" awards full XP without verifying the challenge or quiz were attempted** (found 2026-08-31, fixed 2026-09-13). See docs/REQUIREMENTS.md Fixed bugs for the full writeup.
- [x] F11 Wire the full Professor Python teaching-method prompt into the `/api/tutor` system prompt — Done, verified 2026-08-30
- [x] F16 Student-stated name and learning preference, passed to Professor Python as context — Done, verified 2026-08-30
- [x] F17 Readability pass — Done. Base text raised to 16px / 1.6 line-height; Settings A−/A/A+ text-size control scales lessons, quizzes, tutor chat, and the code editor and persists (`fontSizePreference`).
- [x] **Content-integrity rewrite (all 11 chapters)** — Done 2026-08-31. Not an original F-numbered feature; a substantive fix that came out of testing. An audit found every chapter's sandbox challenge shipped a complete working solution as starter code, and ~3/4 quiz questions per chapter were near-verbatim recall of the lesson text. Every chapter's `challengeCode` is now a comment-only scaffold (student writes the real code), and all quiz questions are scenario/comprehension checks grounded in that chapter's own lesson. Also added a "Practice Challenge Design" rule to `docs/PROFESSOR_PYTHON_PROMPT.md` so the live tutor doesn't hand out minimal-variation copy-the-shape challenges. Sequence: Ch 1 (rewritten, then scope-corrected), Ch 2–5, Ch 6–11.

### Phase 3 — Ideas / someday
- **AI-rewritten "Lecture"-style narration, already generated for all 11 chapters (2026-09-13)** — while sourcing F14b's plain narration audio, Allen tried Speechify's "Podcast"/"Lecture" feature first. It doesn't read the source text verbatim — it rewrites/expands it into its own multi-voice lecture script (confirmed by comparing playback against `narration_scripts/narration_ch1.txt`: the wording doesn't match) - not what F14b needs, since that requires audio synced to the exact narration beats. Kept anyway since Allen likes the result and it's a genuinely different, reusable asset: a **future companion-podcast idea** (an expanded, conversational take on each chapter, distinct from the in-app lesson narration). Not downloadable as a file - Speechify's Podcast feature only offers a share link / RSS feed, no direct export - so these are linked, not stored in the repo:
  - Ch 1 (Hello World): https://speechify.app.link/GW45t93Wo6b
  - Ch 2 (Variables): https://speechify.app.link/vpvZMH7Xo6b
  - Ch 3 (Lists): https://speechify.app.link/6i1I4m9Xo6b
  - Ch 4 (Loops): https://speechify.app.link/RKkaHcaYo6b
  - Ch 5 (if Statements): https://speechify.app.link/29ozy2bYo6b
  - Ch 6 (Dictionaries): https://speechify.app.link/awSKO2bYo6b
  - Ch 7 (While Loops): https://speechify.app.link/igFrGOcYo6b
  - Ch 8 (Functions): https://speechify.app.link/2ERmRydYo6b
  - Ch 9 (Classes): https://speechify.app.link/m1MyK7eYo6b
  - Ch 10 (Files & Exceptions): https://speechify.app.link/41ODLOfYo6b
  - Ch 11 (Testing): https://speechify.app.link/yUQZcEgYo6b
- ~~Cinematic lesson playback with rendered video / generated backgrounds (F12)~~ — superseded by F14; see docs/ARCHITECTURE.md decision note. Not pursued: would require Node.js/FFmpeg (HyperFrames or similar), conflicting with the app's zero-dependency design.
- F10 Embedded lesson videos — folded into F14/lesson content work above
- Chapters 12+ (Pygame, data visualization, web apps) — idea stage, not yet scoped as requirements
- Dark/light theme toggle
- Mobile-friendly layout
- **Natural-sounding voice-to-text / text-to-speech tutor interaction** — explicitly parked, not rejected. A good local voice model or free natural-sounding TTS would conflict with N7 (no runtime beyond browser + Python) and the app's offline, zero-install, USB-portable design. This only makes sense as part of a **separate, hosted web version** of the app (an "extension" product, not the local app) — a server-hosted version could freely call a cloud TTS/voice API without those local constraints. Not scoped or committed to; noted here so the idea isn't lost.
  - **Voice choice, if this ever gets built:** Wyatt (Speechify voice) — chosen by Allen while testing F14b's narration wiring (2026-09-13). Only relevant if this parked idea becomes a real, likely hosted-web-version feature.
- New example code blocks in the tutor chat can be easy to miss mid-conversation, especially in longer responses — worth a visual treatment (border/label) to distinguish a new example from a reference to earlier code. Minor polish, not urgent.

## Next milestone
**v7.0 — achieved and exceeded (2026-08-31):** the original target was Chapter 1's F14 panel working end to end as a proof of concept. It was completed, validated, and then extended to all 11 chapters in the same session, alongside the content-integrity rewrite. Current priorities for what's next: F13 (Projects tab), the free-XP completion bug, and F15 (pending Lottie account check).
