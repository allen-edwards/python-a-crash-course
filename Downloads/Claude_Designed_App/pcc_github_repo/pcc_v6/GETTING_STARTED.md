# Getting Started — Python: A Crash Course

Welcome! This guide walks you through everything from installing the app to using every feature. No prior experience needed.

---

## Table of Contents

1. [Requirements](#1-requirements)
2. [Installation](#2-installation)
3. [Starting the app](#3-starting-the-app)
4. [Your first look — the interface](#4-your-first-look--the-interface)
5. [The sidebar](#5-the-sidebar)
6. [Lessons](#6-lessons)
7. [The sandbox](#7-the-sandbox)
8. [Quizzes and XP](#8-quizzes-and-xp)
9. [AI Tutor](#9-ai-tutor)
10. [Progress tracker](#10-progress-tracker)
11. [Video script generator](#11-video-script-generator)
12. [Settings](#12-settings)
13. [Stopping the app](#13-stopping-the-app)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Requirements

Before you install, make sure you have:

### Python 3.8 or higher

Check if you already have it by opening a terminal and typing:
```bash
python3 --version
```

If you see `Python 3.8.x` or higher you are good to go. If not:

- **Ubuntu/Linux:** `sudo apt install python3 python3-pip python3-venv`
- **macOS:** `brew install python3` or download from [python.org](https://www.python.org/downloads/)
- **Windows:** Download from [python.org](https://www.python.org/downloads/) — during install, make sure to check **"Add Python to PATH"**

### Flask (installed automatically)

Flask is the only dependency and the launcher installs it for you automatically on first run. You don't need to do anything.

### Anthropic API key (optional)

Only needed for the AI Tutor and Video Script Generator features. The rest of the app works completely without it. See [Section 9](#9-ai-tutor) for setup instructions.

---

## 2. Installation

1. Go to the [Releases page](../../releases) and download the latest zip file
2. Extract the zip to a folder you'll remember — for example:
   - Ubuntu: `~/Applications/python-a-crash-course/`
   - Windows: `C:\Users\YourName\Apps\python-a-crash-course\`
   - macOS: `~/Applications/python-a-crash-course/`

Inside the folder you should see:
```
pcc_app/
├── app.py
├── index.html
├── appIcon.png
├── START_MAC_LINUX.sh
├── START_WINDOWS.bat
└── README.txt
```

---

## 3. Starting the app

### Ubuntu / Linux

Open a terminal, navigate to the `pcc_app` folder and run:

```bash
chmod +x START_MAC_LINUX.sh
./START_MAC_LINUX.sh
```

**First run only:** the launcher creates a local Python environment and installs Flask automatically. This takes about 30 seconds and only happens once.

After that your browser opens automatically at `http://127.0.0.1:5757`.

**Also on first run:** a desktop shortcut and app launcher entry are created automatically so you can launch it like any other app in future.

### macOS

Same as Ubuntu — open Terminal, navigate to the folder and run:
```bash
chmod +x START_MAC_LINUX.sh
./START_MAC_LINUX.sh
```

### Windows

Double-click `START_WINDOWS.bat`. If Windows asks "do you want to run this?" click **Run anyway**. Your browser opens automatically.

---

## 4. Your first look — the interface

Once the app opens you will see:

```
┌─────────────────────────────────────────────────────┐
│ ☰  🐍 Python: A Crash Course    0/500 XP  🔥 1d   │  ← Top bar
├──────────────┬──────────────────────────────────────┤
│              │  📖 Lesson  🖥️ Sandbox  🧠 Quiz  🤖 │  ← Tabs
│  Chapters    │                                      │
│  ─────────   │                                      │
│  Ch 1 ✓     │         Main content area            │
│  Ch 2 🔒    │                                      │
│  Ch 3 🔒    │                                      │
│              │                                      │
│  📊 Progress │                                      │
│  ⚙️ Settings │                                      │
└──────────────┴──────────────────────────────────────┘
```

- **Top bar** — app title, XP progress bar, day streak counter
- **Sidebar** — chapter list and navigation
- **Main area** — switches between Lesson, Sandbox, Quiz, and AI Tutor

---

## 5. The sidebar

The sidebar on the left shows all available chapters.

- **Unlocked chapters** — shown normally, click to open
- **Locked chapters** — show 🔒 and the XP needed to unlock them
- **Completed chapters** — show a green ✓

**Collapsing the sidebar:**
Click the **☰** button in the top left to collapse the sidebar and give yourself more screen space. Click it again to bring it back. Useful when you are focused on coding in the sandbox.

---

## 6. Lessons

Each chapter starts with a **Lesson** tab. This is your reading material.

**What you will find:**
- A plain-English explanation of the concept
- Colour-coded code examples showing Python syntax
- Callout boxes highlighting key ideas and warnings
- A 🎬 video placeholder (for future YouTube lesson videos)

**Buttons at the bottom of each lesson:**
- **▶ Try in sandbox** — loads the lesson's example code into the sandbox ready to run
- **📝 Generate video script** — creates an original YouTube script for this chapter (requires API key)
- **✓ Mark complete** — awards XP and marks the chapter done in your progress

**Tip:** Read the lesson first, then click "Try in sandbox" to see the code running, then take the quiz.

**Pop-out lesson panel:**
Click the **⧉ Pop out lesson** button in the sandbox toolbar to open the lesson in a floating window. You can:
- **Drag** it anywhere on screen by clicking and holding the title bar
- **Minimize** it to a small bar using the — button
- **Restore** it by clicking — again
- **Close** it with the ✕ button

This lets you read the lesson and code at the same time side by side.

---

## 7. The sandbox

The sandbox is where you write and run real Python code. It runs directly on your machine using the Python you already have installed — no internet needed.

**Layout:**
- **Left side** — code editor with syntax highlighting
- **Right side** — output panel showing your results

**Syntax highlighting:**
The editor automatically colours your code as you type:
- 🟣 Purple — keywords (`if`, `for`, `def`, `while`)
- 🟡 Yellow — strings (`"hello"`, `'world'`)
- 🔵 Blue — built-in functions (`print`, `len`, `range`)
- 🟠 Orange — numbers (`42`, `3.14`)
- Grey — comments (`# this is a comment`)

**Running code:**
1. Type your Python code in the editor
2. Click **▶ Run** (or press the button)
3. Output appears instantly in the right panel
4. Errors show in red with a description of what went wrong

**Loading chapter examples:**
Click **▶ Try in sandbox** from the lesson tab to pre-load that chapter's example code.

**Loading the challenge:**
Click **Load challenge** to load the chapter's coding challenge — a task that tests what you just learned.

**Copying your code:**
Click **Copy** to copy all code in the editor to your clipboard.

**Clearing the editor:**
Click **Clear** to wipe the editor and start fresh.

**Important:** The terminal window running the app must stay open while you use the sandbox. Closing it stops the server and Run will stop working.

---

## 8. Quizzes and XP

Each chapter has a **Quiz** tab with 4 questions testing what you just learned.

**How it works:**
1. Click a quiz option to answer
2. Green = correct, Red = incorrect
3. The correct answer is always highlighted after you answer
4. Answer all 4 questions to see your result

**Passing:**
Score 3 or more out of 4 to pass and earn XP.

**XP rewards:**
- Completing a lesson = XP (varies by chapter, 15–40 XP)
- Passing a quiz = bonus XP (about 70% of the lesson XP value)
- Total = 500 XP across all 11 chapters

**Unlocking chapters:**
Chapters are locked until you earn enough XP. This encourages you to actually engage with each chapter before moving on rather than skipping ahead.

| Chapter | XP needed to unlock |
|---------|-------------------|
| Ch 1 — Hello World | 0 (free) |
| Ch 2 — Variables | 10 XP |
| Ch 3 — Lists | 20 XP |
| Ch 4 — Loops | 50 XP |
| Ch 5 — if Statements | 90 XP |
| Ch 6 — Dictionaries | 130 XP |
| Ch 7 — While Loops | 180 XP |
| Ch 8 — Functions | 230 XP |
| Ch 9 — Classes | 290 XP |
| Ch 10 — Files & Exceptions | 360 XP |
| Ch 11 — Testing | 430 XP |

**Day streak:**
The 🔥 counter in the top right tracks how many days in a row you have opened the app. Try to keep it going!

**Retrying quizzes:**
You can retry a quiz as many times as you like. XP is only awarded once per chapter though.

---

## 9. AI Tutor

The AI Tutor lets you ask questions about the current chapter in plain English and get clear, friendly explanations.

### Setup (required)

The AI Tutor needs a free Anthropic API key:

1. Go to [console.anthropic.com](https://console.anthropic.com) and create a free account
2. Click **API Keys** in the left sidebar
3. Click **Create Key**, give it a name like `python-app`
4. **Copy the key immediately** — it starts with `sk-ant-...` and you only see it once
5. In the app click **Settings** in the sidebar
6. Paste your key into the API key field and click **Save**

Your key is stored locally on your machine only. It is never sent anywhere except directly to Anthropic's API when you ask a question.

### Using the tutor

1. Open the **🤖 AI Tutor** tab
2. Type your question in the input box at the bottom and press Enter or click **Send**
3. The tutor responds with a short, clear explanation tailored to the current chapter

**Quick prompt buttons:**
Each chapter has 4 suggested questions shown as buttons above the input box. Click any of them to instantly send that question — great for when you are not sure what to ask.

**Example questions to try:**
- *"Explain this to me like I am 10 years old"*
- *"Give me a mini-challenge to practice this"*
- *"Why does Python do it this way?"*
- *"What is the most common mistake beginners make here?"*

**Tips:**
- The tutor knows which chapter you are on and tailors its answers accordingly
- Ask follow-up questions — the tutor remembers the conversation
- If an answer is too long, ask it to summarise in one sentence
- If an answer is too short, ask it to go deeper

---

## 10. Progress tracker

Click **📊 My progress** in the sidebar to see your full progress dashboard.

**What you will see:**
- **Total XP** — how much you have earned out of 500
- **Chapters done** — how many chapters you have completed
- **Quizzes passed** — total quizzes you have passed
- **Day streak** — your current consecutive day streak

**Chapter breakdown:**
A bar for each chapter showing your completion percentage:
- 15% — chapter visited but not completed
- 60% — quiz passed
- 100% — chapter marked complete

**Resetting progress:**
At the bottom of the progress page is a **Reset all progress** button. This clears all XP, streaks, and completion data and starts fresh. Use with caution — this cannot be undone.

---

## 11. Video script generator

Each lesson has a **📝 Generate video script** button that writes an original, copyright-safe YouTube script for that chapter.

### Requirements

- Anthropic API key (see [Section 9](#9-ai-tutor) for setup)

### How to use it

1. Open any lesson
2. Click **📝 Generate video script**
3. Wait 30–60 seconds while the script is generated
4. A window appears with the full script
5. Click **Copy to clipboard**
6. Paste into CapCut, Synthesia, or any video creation tool

### What the script includes

- A proper attribution line crediting the inspiration sources
- Original explanations — no copied text from any book
- Natural, conversational language suitable for AI voiceover
- Scene break markers for video editing tools
- Estimated 8–12 minute video length
- Original code examples throughout

---

## 12. Settings

Click **⚙️ Settings & Credits** in the sidebar.

**API key:**
- Paste your Anthropic API key here to enable the AI Tutor and Script Generator
- Click **Save** to store it
- Click **Clear** to remove it
- Your key is stored in your browser's local storage on your machine only

**Credits:**
The settings page also shows the full credits and acknowledgements for the app including the books that inspired it.

---

## 13. Stopping the app

The app runs as a local server in your terminal window.

**To stop it:**
Press **Ctrl+C** in the terminal window that is running the app.

Your browser tab will show a connection error after this — that is completely normal. Just close the tab.

**Your progress is saved automatically** to a `progress.json` file in the app folder. It is safe to close the app at any time.

---

## 14. Troubleshooting

### Browser does not open automatically
Navigate manually to `http://127.0.0.1:5757`

### "externally-managed-environment" error on Ubuntu
The launcher handles this automatically using a virtual environment. If you see this error, make sure you are running `START_MAC_LINUX.sh` and not `app.py` directly.

### "No module named flask" error
Run this in the `pcc_app` folder:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python app.py
```

### Run button produces no output
Make sure the terminal window is still open and the server is still running. If you closed it, relaunch with `./START_MAC_LINUX.sh`.

### "Port already in use" error
Another instance of the app is already running. Either close that terminal window first, or change the port number in `app.py` — find `port = 5757` near the bottom and change it to any other number like `5758`.

### AI Tutor says "connection error"
- Check your API key is saved correctly in Settings
- Make sure you have an internet connection (the AI needs to reach Anthropic's servers)
- Check your Anthropic account has available credits at [console.anthropic.com](https://console.anthropic.com)

### Desktop shortcut does not work
Make sure the shortcut points to the correct path. Right-click the `.desktop` file → Properties → check the Exec path matches where you extracted the app.

---

*Still stuck? Open an issue at [github.com/allen-edwards/python-a-crash-course/issues](https://github.com/allen-edwards/python-a-crash-course/issues)*
