"""
Python Crash Course - Interactive Learning App
Run with: python app.py  |  Works on Windows, macOS, Ubuntu.
"""
import os, sys, json, threading, webbrowser, time, subprocess
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)
BASE      = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE, "progress.json")
HTML_FILE = os.path.join(BASE, "index.html")

# ── helpers ──────────────────────────────────────────────────────────────────
def load_progress():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"xp":0,"streak":1,"lastActiveDate":None,
            "completed":[],"quizScores":{},"currentChapter":0}

def save_progress(data):
    try:
        with open(SAVE_FILE,"w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# ── routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(HTML_FILE)

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
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=10
        )
        return jsonify({"output": result.stdout, "error": result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "", "error": "Timed out after 10 seconds."})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

@app.route("/api/tutor", methods=["POST"])
def tutor():
    import urllib.request, urllib.error
    body    = request.json
    api_key = body.get("apiKey", "")
    payload = json.dumps({
        "model":    "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system":   body.get("system", ""),
        "messages": body.get("messages", [])
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

# ── start ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = 5757
    print("=" * 55)
    print("  🐍 Python Crash Course — Learning App")
    print(f"  Opening at http://127.0.0.1:{port}")
    print("  Close this window to stop the app.")
    print("=" * 55)
    threading.Thread(target=lambda: (time.sleep(1.2),
        webbrowser.open(f"http://127.0.0.1:{port}")), daemon=True).start()
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

@app.route("/api/generate-script", methods=["POST"])
def generate_script():
    import urllib.request, urllib.error
    body    = request.json
    api_key = body.get("apiKey", "")
    chapter = body.get("chapter", "")
    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 4000,
        "system": """You are an expert Python educator creating original video scripts for a YouTube channel called 'Python: A Crash Course — A Beginner's Journey'. 

IMPORTANT COPYRIGHT RULES:
- Write 100% original content. Do NOT copy or paraphrase text from any book.
- The concepts taught (variables, lists, loops etc) are universal Python knowledge, not owned by anyone.
- At the start of every script include: 'This video is part of the Python: A Crash Course — A Beginner\'s Journey series, inspired by the works of Eric Matthes.'
- Use your own original examples, analogies and explanations.

FORMAT: Write a natural, engaging video script with:
- A warm intro (30 seconds)
- Clear section headers (for CapCut scene breaks)
- Original code examples shown as [CODE: example here]
- Real world analogies to explain concepts
- A summary and call to action at the end
- Estimated duration: 8-12 minutes""",
        "messages": [{"role": "user", "content": f"Write a complete original video script for: {chapter}"}]
    }).encode("utf-8")
    headers = {"Content-Type": "application/json", "anthropic-version": "2023-06-01"}
    if api_key:
        headers["x-api-key"] = api_key
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(c.get("text","") for c in result.get("content",[]))
            return jsonify({"script": text})
    except urllib.error.HTTPError as e:
        return jsonify({"error": e.read().decode("utf-8")}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
