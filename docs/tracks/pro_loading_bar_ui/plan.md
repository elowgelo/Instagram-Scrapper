# Implementation Plan: Professional Loading UI & Dynamic Progress Bar Improvements

## Task List

- [x] Task 1: Redesain Indikator Progress Bar & Button Active State (Anti-Freeze & Shimmer Effect)
  - Detail: Tambahkan efek animasi glowing border & shimmer pulse pada tombol Scrape & progress bar di `index.css`. Pastikan tombol tampak responsif dan tidak terkesan beku.
  - Files: `frontend/src/index.css`, `frontend/src/components/ScrapePanel.jsx`.

- [x] Task 2: Implementasi Logika Progres Dinamis (Smooth Increment & 95% Finalization Cap)
  - Detail: Buat timer progres dinamis yang bergerak mulus (15% -> 40% -> 75% -> 95%) dan tertahan di 95% saat finalisasi backend, lalu secara mulus berubah ke 100% hanya saat data sudah diterima.
  - Files: `frontend/src/components/ScrapePanel.jsx`, `frontend/src/App.jsx`.

- [x] Task 3: Pembaruan Teks Status Teknis SaaS Professional (Non-AI Style)
  - Detail: Ganti istilah yang terlalu kaku/AI dengan frasa log sistem yang bersih, profesional, dan realistis.
  - Files: `frontend/src/components/ScrapePanel.jsx`.

- [x] Task 4: Pengujian & Empiric Verification
  - Detail: Uji alur scraping dengan batas postingan kecil hingga unlimited untuk memastikan animasi progres berjalan halus tanpa lonjakan ke 100% prematur.
