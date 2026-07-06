"""
Launcher for Lab Management System (bundled .exe entry point).

What this does:
  1. Figures out the correct paths (works both when run from source AND inside a
     PyInstaller bundle where __file__ / cwd are different).
  2. Points the database at %APPDATA%\LabManagementSystem\lms.db so it survives
     updates and does not require admin rights.
  3. Starts the FastAPI/uvicorn server in a background thread.
  4. Waits for the server to be ready, then auto-opens the browser.
  5. Shows a small tkinter control window (no console) so the user can open the
     browser again or stop the server cleanly.
"""

import sys
import os

# ── 1. Path setup (MUST happen before any app imports) ────────────────────────
if getattr(sys, "frozen", False):
    # Inside PyInstaller bundle: _MEIPASS holds all bundled files (read-only temp dir)
    BUNDLE_DIR = sys._MEIPASS
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))

# Switch working directory so FastAPI can find templates/ and static/
os.chdir(BUNDLE_DIR)

# ── 2. Writable data directory in AppData ─────────────────────────────────────
APPDATA = os.environ.get("APPDATA", os.path.expanduser("~"))
DATA_DIR = os.path.join(APPDATA, "LabManagementSystem")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "lms.db")
is_first_run = not os.path.exists(DB_PATH)

# Inject env vars before importing the app (dotenv will not override these)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{DB_PATH}")
os.environ.setdefault("SECRET_KEY", "lms-offline-key-please-change-me")
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "admin123")

# ── 3. Imports (app modules are now on the path) ───────────────────────────────
import threading
import time
import webbrowser
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox
import uvicorn

PORT = 8001
APP_URL = f"http://localhost:{PORT}"


# ── 4. Server ──────────────────────────────────────────────────────────────────
def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, log_level="error")


def wait_and_open_browser():
    """Poll until the server responds, then open the default browser."""
    for _ in range(60):           # wait up to 30 seconds
        try:
            urllib.request.urlopen(APP_URL, timeout=1)
            webbrowser.open(APP_URL)
            return
        except Exception:
            time.sleep(0.5)
    messagebox.showerror(
        "Lab Management System",
        f"Server did not start in time.\nTry opening {APP_URL} manually."
    )


server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

browser_thread = threading.Thread(target=wait_and_open_browser, daemon=True)
browser_thread.start()


# ── 5. Tkinter control window ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Lab Management System")
root.geometry("340x200")
root.resizable(False, False)

# Try to set window icon if bundled
try:
    icon_path = os.path.join(BUNDLE_DIR, "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
except Exception:
    pass

# Keep window on top initially so user notices it
root.lift()
root.attributes("-topmost", True)
root.after(3000, lambda: root.attributes("-topmost", False))

style = ttk.Style()
style.theme_use("vista")

frame = ttk.Frame(root, padding=24)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(
    frame,
    text="Lab Management System",
    font=("Segoe UI", 14, "bold"),
).pack()

status_var = tk.StringVar(value="Starting server…")
status_label = ttk.Label(frame, textvariable=status_var, foreground="gray")
status_label.pack(pady=(4, 16))


def update_status():
    try:
        urllib.request.urlopen(APP_URL, timeout=1)
        status_var.set("✓  Server is running")
        status_label.configure(foreground="green")
    except Exception:
        root.after(800, update_status)


root.after(800, update_status)


def open_browser():
    webbrowser.open(APP_URL)


open_btn = ttk.Button(frame, text="Open in Browser", command=open_browser)
open_btn.pack(fill=tk.X, pady=3)

stop_btn = ttk.Button(frame, text="Stop & Exit", command=root.destroy)
stop_btn.pack(fill=tk.X, pady=3)

ttk.Label(
    frame,
    text=f"Running at {APP_URL}",
    foreground="gray",
    font=("Segoe UI", 8),
).pack(pady=(8, 0))

root.mainloop()
# Daemon threads stop automatically when the main thread exits.
