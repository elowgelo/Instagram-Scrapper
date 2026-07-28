"""
===================================================================
📸 INSTAGRAM SCRAPER & KEYWORD FILTER ENGINE - DESKTOP LAUNCHER
===================================================================
Skrip ini menyalakan server backend FastAPI dan secara otomatis 
membuka antarmuka aplikasi web di browser default pengguna.
"""

import os
import sys
import time
import subprocess
import webbrowser
import threading
import uvicorn

# Ensure backend folder is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

def kill_existing_port_8000():
    try:
        cmd = 'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :8000 ^| findstr LISTENING\') do taskkill /f /pid %a'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def open_browser():
    time.sleep(1.8)
    url = "http://127.0.0.1:8000"
    print(f"\n🚀 Membuka Instagram Scraper Desktop App di browser: {url}")
    webbrowser.open(url)

def main():
    print("===================================================================")
    print("📸 INSTAGRAM SCRAPER & KEYWORD FILTER ENGINE (DESKTOP EDITION)")
    print("===================================================================")
    print("Menyalakan server lokal di http://127.0.0.1:8000 ...")
    
    kill_existing_port_8000()
    time.sleep(0.5)
    
    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Uvicorn Server
    from main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
