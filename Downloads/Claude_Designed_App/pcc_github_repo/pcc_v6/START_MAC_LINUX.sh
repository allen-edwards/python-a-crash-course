#!/bin/bash
# Python: A Crash Course — A Beginner's Journey
# Launcher for macOS and Ubuntu/Linux

echo ""
echo " ============================================="
echo "  🐍 Python: A Crash Course — A Beginner's Journey"
echo " ============================================="
echo ""

# ── Find Python 3 ─────────────────────────────────────────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER=$("$cmd" -c "import sys; print(sys.version_info.major)" 2>/dev/null)
        if [ "$VER" = "3" ]; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo " ERROR: Python 3 not found!"
    echo ""
    echo "   macOS:  brew install python3"
    echo "   Ubuntu: sudo apt install python3 python3-pip python3-venv"
    echo ""
    read -p " Press Enter to exit..."
    exit 1
fi

echo " Using: $($PYTHON --version)"

# ── App directory ─────────────────────────────────────────────────────────────
APP_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Virtual environment setup ─────────────────────────────────────────────────
VENV_DIR="$APP_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo " Setting up local Python environment (one-time setup)..."
    $PYTHON -m venv "$VENV_DIR" 2>/tmp/venv_err.log
    if [ $? -ne 0 ]; then
        echo " ERROR: Could not create virtual environment."
        echo " On Ubuntu run: sudo apt install python3-venv"
        cat /tmp/venv_err.log
        read -p " Press Enter to exit..."
        exit 1
    fi
fi

source "$VENV_DIR/bin/activate"

python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " Installing Flask (one-time setup)..."
    pip install --quiet --upgrade pip
    pip install --quiet flask
fi

# ── Auto-create desktop launcher (Linux only) ─────────────────────────────────
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    DESKTOP_FILE="$HOME/Desktop/Python_A_Crash_Course.desktop"
    APP_LAUNCHER="$HOME/.local/share/applications/Python_A_Crash_Course.desktop"
    ICON_PATH="$APP_DIR/appIcon.png"
    EXEC_CMD="bash -c \"'$APP_DIR/START_MAC_LINUX.sh'; echo; echo 'Press Enter to close...'; read\""

    DESKTOP_CONTENT="[Desktop Entry]
Type=Application
Name=Python: A Crash Course
Comment=A Beginner's Journey — Learn Python interactively
Exec=bash -c \"'$APP_DIR/START_MAC_LINUX.sh'; echo; echo 'Press Enter to close...'; read\"
Icon=$ICON_PATH
Terminal=true
Categories=Education;Programming;
Keywords=python;learn;code;programming;"

    # Create on Desktop if it exists
    if [ -d "$HOME/Desktop" ]; then
        echo "$DESKTOP_CONTENT" > "$DESKTOP_FILE"
        chmod +x "$DESKTOP_FILE"
        # Trust it (GNOME)
        gio set "$DESKTOP_FILE" metadata::trusted true 2>/dev/null || true
        echo " ✓ Desktop shortcut created"
    fi

    # Install into app launcher (~/.local/share/applications)
    mkdir -p "$HOME/.local/share/applications"
    echo "$DESKTOP_CONTENT" > "$APP_LAUNCHER"
    chmod +x "$APP_LAUNCHER"
    # Refresh app menu
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    echo " ✓ App launcher entry created"
fi

# ── macOS: create .command launcher on Desktop ────────────────────────────────
if [[ "$OSTYPE" == "darwin"* ]]; then
    MAC_LAUNCHER="$HOME/Desktop/Python A Crash Course.command"
    if [ ! -f "$MAC_LAUNCHER" ]; then
        echo "#!/bin/bash" > "$MAC_LAUNCHER"
        echo "cd '$APP_DIR' && ./START_MAC_LINUX.sh" >> "$MAC_LAUNCHER"
        chmod +x "$MAC_LAUNCHER"
        echo " ✓ Desktop launcher created (macOS)"
    fi
fi

# ── Launch the app ────────────────────────────────────────────────────────────
echo ""
echo " Starting app — your browser will open automatically."
echo " Press Ctrl+C to stop the server."
echo ""
cd "$APP_DIR"
python app.py
