# Track Spec: Multi-User Session Isolation & Collision Prevention

## Goal
Mencegah terjadinya bentrokan data (data collision) antar pengguna yang mengakses aplikasi secara bersamaan (di HP, Laptop, atau banyak pengguna sekaligus) dengan menerapkan Client Session Isolation.

## Scope & Requirements
1. **Client Session Token (UUID)**:
   - Setiap browser/klien secara otomatis menghasilkan session_token (UUID) yang unik saat pertama kali membuka aplikasi.
2. **Database Session Scoping (storage.py & main.py)**:
   - Kolom session_token ditambahkan pada tabel SQLite posts.
   - Endpoint /api/scrape, /api/posts, /api/filter, dan /api/posts (DELETE) hanya akan membaca, menyimpan, dan menghapus data postingan yang sesuai dengan session_token pengguna tersebut.
3. **Pembersihan Data Independen**:
   - Saat pengguna di HP menekan "Bersihkan Data", hanya data di HP-nya yang terhapus. Data pengguna di Laptop tidak akan ikut terhapus.
