# Track Spec: Standalone Windows EXE Desktop App Build

## Goal
Mengemas seluruh aplikasi (FastAPI Backend + React Frontend + Chromium Engine) menjadi Satu File Executable Windows (`InstagramScraper.exe`) atau launcher 1-klik yang dapat dijalankan langsung di komputer Windows tanpa dependensi external.

## Scope & Requirements
1. **PyInstaller Packaging (build_exe.py)**:
   - Mengompilasi FastAPI backend dan aset statis React (`frontend/dist`) menjadi bundle file executable mandiri.
2. **Auto Browser Launcher (launcher.py)**:
   - Saat aplikasi dijalankan, server backend menyala dan otomatis membuka browser pengguna ke `http://127.0.0.1:8000`.
3. **Penyimpanan Lokal & 100% Bebas IP Limit**:
   - SQLite database disimpan di folder aplikasi lokal. Pengguna dapat meng-scrape 1.000+ postingan tanpa batasan IP cloud.
