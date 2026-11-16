"""
Python: A Crash Course — A Beginner's Journey
Run with: python app.py  |  Works on Windows, macOS, Ubuntu.
"""
import os, sys, json, shutil, threading, webbrowser, time, subprocess
from flask import Flask, send_file, request, jsonify, send_from_directory

app = Flask(__name__)
BASE      = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE, "progress.json")
HTML_FILE = os.path.join(BASE, "index.html")
VENDOR    = os.path.join(BASE, "vendor")
AUDIO     = os.path.join(BASE, "audio")

# ── helpers ───────────────────────────────────────────────────────────────────
DEFAULT_PROGRESS = {"xp":0,"streak":1,"lastActiveDate":None,
                    "completed":[],"quizScores":{},"currentChapter":0,
                    "studentName":"","learningPreference":"",
                    "fontSizePreference":"medium"}

def load_progress():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE) as f:
                data = json.load(f)
            if isinstance(data, dict):
                # merge onto defaults so older save files missing newer
                # fields (e.g. studentName / learningPreference) still load
                return {**DEFAULT_PROGRESS, **data}
    except Exception:
        pass
    return dict(DEFAULT_PROGRESS)

def save_progress(data):
    try:
        with open(SAVE_FILE,"w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# Automatic backups: before any action that resets or rewrites progress (Reset my progress, the
# one-time XP migration, a future Load progress file) the page asks the server to copy
# progress.json to progress.bak1.json, rotating the older copies and keeping the last 3.
# Backups live in the app folder and are git-ignored like progress.json. The tutor API key is
# stored in the browser, never in progress.json, so it can never end up in a backup.
BACKUP_KEEP = 3

def backup_progress():
    """Returns (ok, error). Nothing to back up (no save file yet) counts as ok."""
    if not os.path.exists(SAVE_FILE):
        return True, None
    try:
        for i in range(BACKUP_KEEP, 1, -1):
            older = os.path.join(BASE, "progress.bak%d.json" % (i-1))
            newer = os.path.join(BASE, "progress.bak%d.json" % i)
            if os.path.exists(older):
                os.replace(older, newer)
        shutil.copy2(SAVE_FILE, os.path.join(BASE, "progress.bak1.json"))
        return True, None
    except Exception as e:
        return False, str(e)

# Restore from a backup (Settings, next to Reset). The page lists the backups, each one is checked
# before it is offered, and a restore first keeps the CURRENT progress as progress.prerestore.json,
# a separate copy outside the rotation, so restoring can itself be undone (and the backup being
# restored is never pushed out by that copy). A restore brings back what Reset clears (XP, chapters,
# quiz scores, streak, challenge flags, current chapter) and leaves the name, learning preference and
# text size as they are now. Only fixed slot names are ever read; the page never supplies a path.
CHAPTER_COUNT = 11          # must match CHAPTERS in index.html
RESTORE_SLOTS = ["bak1", "bak2", "bak3", "prerestore"]
PRERESTORE_FILE = os.path.join(BASE, "progress.prerestore.json")
RESTORE_FIELDS = ["xp", "streak", "lastActiveDate", "completed", "quizScores", "challengeRun",
                  "cur", "currentChapter", "xpModel"]

def slot_path(slot):
    if slot == "prerestore":
        return PRERESTORE_FILE
    return os.path.join(BASE, "progress.%s.json" % slot)

def check_progress(data):
    """Returns (ok, reason, summary). A backup that fails is shown as damaged and cannot be chosen."""
    if not isinstance(data, dict):
        return False, "not a progress file", None
    xp = data.get("xp")
    if isinstance(xp, bool) or not isinstance(xp, (int, float)) or not 0 <= xp <= 500:
        return False, "XP is missing or out of range", None
    done = data.get("completed")
    if not isinstance(done, list) or any(isinstance(c, bool) or not isinstance(c, int)
                                         or not 0 <= c < CHAPTER_COUNT for c in done):
        return False, "completed chapters are missing or invalid", None
    quiz = data.get("quizScores", {})
    if not isinstance(quiz, dict) or any(
            not str(k).isdigit() or int(k) >= CHAPTER_COUNT or isinstance(v, bool)
            or not isinstance(v, (int, float)) or v < 0 for k, v in quiz.items()):
        return False, "quiz scores are invalid", None
    streak = data.get("streak", 1)
    if isinstance(streak, bool) or not isinstance(streak, int) or not 0 <= streak <= 100000:
        return False, "streak is invalid", None
    if "challengeRun" in data and not isinstance(data["challengeRun"], dict):
        return False, "challenge records are invalid", None
    if data.get("xpModel", 1) not in (1, 2):
        return False, "unknown XP model", None
    return True, None, {"xp": int(xp), "chapters": len(set(done)),
                        "quizzes": sum(1 for v in quiz.values() if v >= 3)}

def read_slot(slot):
    path = slot_path(slot)
    if not os.path.exists(path):
        return None
    info = {"slot": slot, "modified": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(path)))}
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        info.update(ok=False, reason="the file cannot be read", summary=None)
        return info, None
    ok, reason, summary = check_progress(data)
    info.update(ok=ok, reason=reason, summary=summary)
    return info, data

# ── routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(HTML_FILE)

@app.route("/vendor/<path:filename>")
def vendor(filename):
    return send_from_directory(VENDOR, filename)

@app.route("/audio/<path:filename>")
def audio(filename):
    return send_from_directory(AUDIO, filename)

@app.route("/api/progress", methods=["GET"])
def get_progress():
    return jsonify(load_progress())

@app.route("/api/progress", methods=["POST"])
def set_progress():
    save_progress(request.json)
    return jsonify({"ok": True})

@app.route("/api/progress/backup", methods=["POST"])
def backup_progress_route():
    ok, err = backup_progress()
    if ok:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": err}), 500

@app.route("/api/progress/backups", methods=["GET"])
def list_backups():
    out = []
    for slot in RESTORE_SLOTS:
        got = read_slot(slot)
        if got:
            out.append(got[0])
    ok, _, summary = check_progress(load_progress())
    return jsonify({"backups": out, "current": summary if ok else None})

@app.route("/api/progress/restore", methods=["POST"])
def restore_progress():
    slot = (request.json or {}).get("slot", "")
    if slot not in RESTORE_SLOTS:
        return jsonify({"ok": False, "error": "unknown backup"}), 400
    got = read_slot(slot)
    if not got:
        return jsonify({"ok": False, "error": "that backup no longer exists"}), 404
    info, data = got
    if not info["ok"]:
        return jsonify({"ok": False, "error": "that backup is damaged: " + str(info["reason"])}), 400
    try:
        if os.path.exists(SAVE_FILE):
            shutil.copy2(SAVE_FILE, PRERESTORE_FILE)    # keep what is there now, so this can be undone
        current = load_progress()
        for field in RESTORE_FIELDS:
            current.pop(field, None)
        current.update({k: v for k, v in data.items() if k in RESTORE_FIELDS})
        with open(SAVE_FILE, "w") as f:      # not save_progress(): a failed restore must say so
            json.dump(current, f, indent=2)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    return jsonify({"ok": True})

@app.route("/api/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")
    # Simulated stdin for input() - one line per call, typed by the student
    # in the sandbox's "simulated input" box. Passing `input=` to
    # subprocess.run() feeds it to the child's stdin and closes the pipe
    # once it's written - the standard technique for a one-shot,
    # non-interactive subprocess. A blank simulated_input is harmless for
    # code that never calls input() (stdin is simply never read), so this
    # is not a behavior change for the common no-input() case.
    simulated_input = request.json.get("simulatedInput", "") or ""
    if simulated_input and not simulated_input.endswith("\n"):
        simulated_input += "\n"  # last input() call still gets a trailing newline, like a real terminal
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            input=simulated_input, capture_output=True, text=True, timeout=10
        )
        return jsonify({"output": result.stdout, "error": result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Timed out after 10 seconds. If your code uses input(), make sure you've provided enough simulated input lines above - each input() call needs its own line."})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

@app.route("/api/tutor", methods=["POST"])
def tutor():
    import urllib.request, urllib.error
    body    = request.json
    api_key = body.get("apiKey", "")
    payload = json.dumps({
        "model":      "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system":     body.get("system", ""),
        "messages":   body.get("messages", [])
    }).encode("utf-8")
    headers = {"Content-Type": "application/json",
               "anthropic-version": "2023-06-01"}
    if api_key:
        headers["x-api-key"] = api_key
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(c.get("text","") for c in result.get("content",[]))
            return jsonify({"text": text})
    except urllib.error.HTTPError as e:
        return jsonify({"error": e.read().decode("utf-8")}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── start — MUST be last ──────────────────────────────────────────────────────
if __name__ == "__main__":
    port = 5757
    print("=" * 55)
    print("  🐍 Python: A Crash Course — A Beginner's Journey")
    print(f"  Opening at http://127.0.0.1:{port}")
    print("  Press Ctrl+C to stop the app.")
    print("=" * 55)
    threading.Thread(
        target=lambda: (time.sleep(1.2), webbrowser.open(f"http://127.0.0.1:{port}")),
        daemon=True
    ).start()
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
