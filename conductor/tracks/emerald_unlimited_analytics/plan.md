# Implementation Plan: Unlimited Scraping, Emerald SaaS UI, Analytics & Substring Filter

## Task List

- [x] Task 1: Update Backend Scraper (Unlimited Mode, Username Penulis Asli & Jumlah Like/Komen)
  - Detail: Perbarui `playwright_scraper.py` untuk mengekstrak username penulis akun Instagram asli (bukan hashtag), jumlah Like & Komentar real, serta mendukung scrolling mode `Tidak Terbatas`.
  - Files: `backend/playwright_scraper.py`, `backend/models.py`, `backend/main.py`.

- [x] Task 2: Substring & Numeric Keyword Matching Engine
  - Detail: Perbarui `filter_engine.py` & komponen penyorot teks agar pencarian potongan kata (misal `"ra"`) atau potongan angka (misal `"2026"` atau `"50"`) dapat dicocokkan dan disorot dengan sempurna.
  - Files: `backend/filter_engine.py`, `frontend/src/components/PostCard.jsx`, `frontend/src/components/PostTable.jsx`.

- [x] Task 3: Redesain UI Emerald SaaS Theme & Cleanup Tab Impor
  - Detail: Hapus tab impor manual. Ubah warna tombol & aksen menjadi skema **Emerald Professional SaaS (`#10b981` / `#059669`)** yang mahal, bersih, dan tampak profesional.
  - Files: `frontend/src/index.css`, `frontend/src/components/Navbar.jsx`, `frontend/src/components/ScrapePanel.jsx`, `frontend/src/App.jsx`.

- [x] Task 4: Fitur Tambahan (Sort Analytics & Quick Copy Caption)
  - Detail: Tambahkan opsi pengurutan postingan (Paling Banyak Like, Paling Banyak Komentar, Terbaru) & tombol 1-Click Salin Caption pada kartu postingan.
  - Files: `frontend/src/components/KeywordFilterBar.jsx`, `frontend/src/components/PostCard.jsx`, `frontend/src/App.jsx`.

- [x] Task 5: Pengujian & Empiric Verification
  - Detail: Verifikasi akhir scraping unlimited, ekstraksi username & statistik, substring/numeric matching, dan tampilan UI Emerald.
