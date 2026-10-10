#!/usr/bin/env bash
# Builds "Tiger CAT.app" in cat/ (the app folder inside the skills repository): a double-clickable launcher
# that starts the local server (cat/tools/serve.py) and opens the app in the default browser. The launcher
# finds cat/ as the bundle's parent, so the .app keeps working wherever the repository is checked out.
# No Xcode, node or Rust needed. Also run by ./install.sh --cat.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="$ROOT/Tiger CAT.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"
cat > "$APP/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>CFBundleName</key><string>Tiger CAT</string>
  <key>CFBundleDisplayName</key><string>Tiger CAT</string>
  <key>CFBundleIdentifier</key><string>org.tigercat.app</string>
  <key>CFBundleVersion</key><string>0.2</string>
  <key>CFBundleShortVersionString</key><string>0.2</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>launch</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
  <key>LSUIElement</key><true/>
</dict></plist>
EOF
cat > "$APP/Contents/MacOS/launch" <<'EOF'
#!/usr/bin/env bash
# Tiger CAT launcher: find the app folder cat/ (this bundle sits inside it), make sure Python has what the
# app needs, start the server if it is not running, open the browser.
set -u
BUNDLE="$(cd "$(dirname "$0")/../.." && pwd)"
ROOT="$(cd "$BUNDLE/.." && pwd)"
PORT="${VCAT_PORT:-8765}"
LOG="$HOME/Library/Logs/TigerCAT.log"
mkdir -p "$(dirname "$LOG")"
notify() { osascript -e "display notification \"$1\" with title \"Tiger CAT\"" >/dev/null 2>&1 || true; }
PY=""
for c in /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 python3; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' 2>/dev/null; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then notify "Python 3.9 or newer is needed (install Xcode Command Line Tools or Homebrew python)."; exit 1; fi
VENV="$HOME/.venvs/vcat"
if [ ! -x "$VENV/bin/python3" ]; then
  notify "First start: preparing Python packages (one minute)…"
  "$PY" -m venv "$VENV" >>"$LOG" 2>&1 || { notify "Could not create a Python environment; see $LOG"; exit 1; }
fi
"$VENV/bin/python3" -c 'import docx, pyewts' 2>/dev/null || "$VENV/bin/pip" install -q --upgrade pip python-docx pyewts >>"$LOG" 2>&1 || notify "Package install had a problem; see $LOG"
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/api/projects"; then
  cd "$ROOT"
  nohup "$VENV/bin/python3" "$ROOT/tools/serve.py" --port "$PORT" >>"$LOG" 2>&1 &
  for i in $(seq 1 40); do sleep 0.25; curl -s -o /dev/null "http://127.0.0.1:$PORT/api/projects" && break; done
fi
[ -n "${VCAT_NO_OPEN:-}" ] || open "http://127.0.0.1:$PORT/"
EOF
chmod +x "$APP/Contents/MacOS/launch"
# a plain icon: the Tibetan letter ka on a dark square, rendered with the system tools if available
if command -v sips >/dev/null 2>&1 && command -v iconutil >/dev/null 2>&1; then
  TMP="$(mktemp -d)"; mkdir -p "$TMP/icon.iconset"
  cat > "$TMP/icon.svg" <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"><rect width="1024" height="1024" rx="220" fill="#8a4b2a"/><text x="512" y="700" font-family="Kokonor, Kailasa, serif" font-size="560" fill="#fff" text-anchor="middle">ཀ</text></svg>
EOF
  if command -v qlmanage >/dev/null 2>&1; then
    qlmanage -t -s 1024 -o "$TMP" "$TMP/icon.svg" >/dev/null 2>&1 || true
    if [ -f "$TMP/icon.svg.png" ]; then
      for s in 16 32 64 128 256 512; do sips -z $s $s "$TMP/icon.svg.png" --out "$TMP/icon.iconset/icon_${s}x${s}.png" >/dev/null 2>&1; done
      cp "$TMP/icon.svg.png" "$TMP/icon.iconset/icon_512x512@2x.png"
      iconutil -c icns "$TMP/icon.iconset" -o "$APP/Contents/Resources/icon.icns" 2>/dev/null && /usr/libexec/PlistBuddy -c "Add :CFBundleIconFile string icon" "$APP/Contents/Info.plist" >/dev/null 2>&1 || true
    fi
  fi
  rm -rf "$TMP"
fi
touch "$APP"
echo "built: $APP"
