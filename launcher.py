"""
launcher.py - Entry point for the Lab Management System (Windows)
- Starts the FastAPI/uvicorn server in a background thread
- Opens the browser automatically
- Shows a system tray icon with a Quit option
"""

import sys
import os

# Fix for PyInstaller windowed mode — stdout/stderr are None
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")



import threading
import webbrowser
import time

# ── Path fix for PyInstaller bundled app ────────────────────────────────────
# When frozen, sys._MEIPASS holds the extracted bundle folder.
# We set the working directory there so SQLite DB and templates are found.
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    # The DB should live next to the .exe, not inside the bundle
    EXE_DIR = os.path.dirname(sys.executable)
    os.chdir(BASE_DIR)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR = BASE_DIR
    os.chdir(BASE_DIR)

# ── Config ───────────────────────────────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 8001
APP_NAME = "Lab Management System"
APP_URL = f"http://{HOST}:{PORT}"

# ── Tray icon image (drawn with Pillow — no external image file needed) ──────
def create_tray_image():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (64, 64), color=(20, 100, 180))
    draw = ImageDraw.Draw(img)
    # Simple "LMS" cross / flask icon
    draw.rectangle([28, 10, 36, 54], fill=(255, 255, 255))
    draw.rectangle([14, 28, 50, 36], fill=(255, 255, 255))
    return img

# ── Start uvicorn server ─────────────────────────────────────────────────────
def start_server():
    import uvicorn
    import main as app_module
    uvicorn.run(
        app_module.app,      # ← pass object directly, not "main:app" string
        host=HOST,
        port=PORT,
        log_level="warning",
    )

# ── Wait for server to be ready, then open browser ──────────────────────────
def open_browser_when_ready():
    import urllib.request
    for _ in range(20):          # Try for ~10 seconds
        try:
            urllib.request.urlopen(APP_URL, timeout=1)
            webbrowser.open(APP_URL)
            return
        except Exception:
            time.sleep(0.5)

# ── System tray ─────────────────────────────────────────────────────────────
def run_tray():
    import pystray

    def on_open(icon, item):
        webbrowser.open(APP_URL)

    def on_quit(icon, item):
        icon.stop()
        # Give tray a moment to close cleanly, then force-exit
        time.sleep(0.3)
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Open in Browser", on_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", on_quit),
    )

    icon = pystray.Icon(
        APP_NAME,
        icon=create_tray_image(),
        title=APP_NAME,
        menu=menu,
    )
    icon.run()   # Blocks until on_quit calls icon.stop()

# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Start FastAPI server in a daemon thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 2. Open browser once server is up (non-blocking)
    browser_thread = threading.Thread(target=open_browser_when_ready, daemon=True)
    browser_thread.start()

    # 3. Run system tray (blocks main thread — keeps app alive)
    run_tray()