# Contributing

Thanks for your interest in contributing to **Python: A Crash Course — A Beginner's Journey**!

This started as a personal learning project, and any contributions that make it better for beginners are very welcome.

---

## Ways to contribute

- 🐛 **Bug reports** — open an Issue describing what went wrong and how to reproduce it
- 💡 **Feature ideas** — open an Issue with your suggestion
- 📖 **Lesson improvements** — better explanations, clearer examples, fixing typos
- 🧪 **New quiz questions** — more variety helps learners
- 🌍 **Translations** — help make this accessible in other languages

---

## Ground rules

1. All lesson content must be **original** — do not copy text from any published book
2. Code examples should be clear, beginner-friendly, and runnable
3. Be kind — this project is for people learning to code for the first time
4. Credit any inspiration sources in your PR description

---

## How to submit a pull request

1. Fork the repository
2. Create a new branch: `git checkout -b your-feature-name`
3. Make your changes
4. Test that the app still runs correctly with `python app.py`
5. Submit a pull request with a clear description of what you changed and why

---

## Running locally for development

```bash
git clone https://github.com/YOUR_USERNAME/python-a-crash-course.git
cd python-a-crash-course
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install flask
python app.py
```

Then open `http://127.0.0.1:5757` in your browser.
