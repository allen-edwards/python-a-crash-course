"""
Python: A Crash Course — A Beginner's Journey
Run with: python app.py  |  Works on Windows, macOS, Ubuntu.
"""
import os, sys, json, threading, webbrowser, time, subprocess
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

# ARCHIVED FEATURE, NOT CURRENTLY IN USE — kept intact, disconnected from UI.
# Original purpose: generate a YouTube-style video script per chapter, for
# Allen to record and host on a YouTube channel. Superseded by F14 (in-app
# Video mode) — Allen decided against a YouTube channel (external dependency
# risk: policy changes, copyright strikes outside his control).
# Decision point: if this route is still unused by v8.0, remove it entirely
# along with any related frontend code. If a real future use emerges before
# then, this comment can simply be deleted.
@app.route("/api/generate-script", methods=["POST"])
def generate_script():
    import urllib.request, urllib.error
    body    = request.json
    api_key = body.get("apiKey", "")
    chapter = body.get("chapter", "")
    payload = json.dumps({
        "model":      "claude-sonnet-4-6",
        "max_tokens": 4000,
        "system": (
            "You are an expert Python educator creating original video scripts "
            "for a YouTube channel called 'Python: A Crash Course — A Beginner's Journey'.\n\n"
            "IMPORTANT:\n"
            "- Write 100% original content. Do NOT copy from any book.\n"
            "- Start every script with: 'This video is part of the Python: A Crash Course "
            "series, inspired by the works of Eric Matthes.'\n"
            "- Use your own original examples and analogies.\n\n"
            "FORMAT:\n"
            "- Warm intro (30 seconds)\n"
            "- Clear section headers for CapCut scene breaks\n"
            "- Code examples shown as [CODE: example here]\n"
            "- Real world analogies\n"
            "- Summary and call to action at the end\n"
            "- Aim for 8-12 minutes"
        ),
        "messages": [{"role": "user", "content": f"Write a complete original video script for: {chapter}"}]
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
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(c.get("text","") for c in result.get("content",[]))
            return jsonify({"script": text})
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
