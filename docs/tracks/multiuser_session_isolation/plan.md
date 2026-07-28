# Implementation Plan: Multi-User Session Isolation & Collision Prevention

## Task List

- [ ] Task 1: Update SQLite Database Storage & Scoping (`storage.py` & `models.py`)
  - Detail: Tambahkan kolom `session_token` pada tabel `posts`. Perbarui fungsi `save_posts_to_db`, `get_all_posts_from_db`, dan `clear_all_posts_in_db` agar menerima parameter `session_token`.
  - Files: `backend/storage.py`, `backend/models.py`.

- [ ] Task 2: Update Endpoint API Backend (`main.py`)
  - Detail: Sesuaikan endpoint `/api/scrape`, `/api/posts`, `/api/filter`, dan `/api/posts` (DELETE) agar membaca header / query `session_token` dari request pengguna.
  - Files: `backend/main.py`.

- [ ] Task 3: Implementasi Automatic Session Token pada React Frontend (`App.jsx` & `Navbar.jsx`)
  - Detail: Hasilkan `session_token` otomatis via `crypto.randomUUID()` di `App.jsx`, dan sertakan pada setiap panggilan API backend.
  - Files: `frontend/src/App.jsx`, `frontend/src/components/Navbar.jsx`.

- [ ] Task 4: Pengujian Multi-Session & Re-deploy
  - Detail: Uji coba simulasi 2 session independen, jalankan `npm run build` frontend, dan push perbaikan ke GitHub untuk re-deploy di Vercel & Render.
