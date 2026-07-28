# Implementation Plan: Standalone Windows EXE Desktop App Build

## Task List

- [x] Task 1: Konfigurasi Static File Serving pada FastAPI Backend (`main.py`)
  - Detail: Tambahkan handler static files untuk melayani `frontend/dist` secara langsung dari FastAPI backend agar backend dan frontend berjalan di 1 port bersama (`http://127.0.0.1:8000`).
  - Files: `backend/main.py`.

- [x] Task 2: Buat Script Auto Launcher & PyInstaller Spec (`launcher.py` & `build_exe.py`)
  - Detail: Buat file `launcher.py` yang menyalakan server uvicorn dan otomatis membuka browser pengguna ke `http://127.0.0.1:8000`. Buat skrip pembangun `build_exe.py` menggunakan PyInstaller.
  - Files: `launcher.py`, `build_exe.py`.

- [x] Task 3: Kompilasi & Packaging Standalone `.EXE` (`dist/InstagramScraper.exe`)
  - Detail: Jalankan `npm run build` frontend, pasang `pyinstaller`, dan eksekusi kompilasi menjadi file executable `.exe`.
  - Files: `dist/InstagramScraper.exe`.

- [x] Task 4: Pengujian & Pembuatan Panduan Windows EXE
  - Detail: Uji eksekusi file `.exe`, buat skrip 1-klik tambahan `run_app.bat` sebagai alternatif launcher cepat, dan update dokumentasi README.md.
