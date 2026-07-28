# Implementation Plan: Hashtag Scraping Fix, Theme Toggle, & Scraper UI Enhancements

## Task List

- [x] Task 1: Perbaikan Backend Scraper (Hashtag `#` Scraping & Strict Failure Status)
  - Detail: Update Playwright scraper untuk menangani URL hashtag `https://www.instagram.com/explore/tags/<tag>/`. Hapus generator data demo acak dari `scraper.py`, dan kembalikan exception status gagal yang jelas jika di-blokir.
  - Files: `backend/playwright_scraper.py`, `backend/scraper.py`, `backend/main.py`.

- [x] Task 2: Implementasi Sistem Dual Theme (Dark & Light Mode UI)
  - Detail: Tambahkan variabel CSS tema terang & gelap di `index.css`. Tambahkan tombol Toggle Theme (Sun/Moon icon) di `Navbar.jsx` dengan memori `localStorage`.
  - Files: `frontend/src/index.css`, `frontend/src/components/Navbar.jsx`, `frontend/src/App.jsx`.

- [x] Task 3: Peningkatan UI Scrape Panel (Limit 100 Post & Live Progress Bar)
  - Detail: Perbarui opsi dropdown limit hingga 100 postingan. Tambahkan indikator progress bar / status real-time saat scraping berjalan.
  - Files: `frontend/src/components/ScrapePanel.jsx`, `frontend/src/App.jsx`.

- [x] Task 4: Code Cleanup & Refactoring
  - Detail: Hapus modul demo/palsu yang tidak diperlukan agar codebase bersih dan terfokus.
  - Files: `backend/scraper.py`, `frontend/src/components/ScrapePanel.jsx`.

- [x] Task 5: Pengujian & Empiric Verification
  - Detail: Verifikasi akhir scraping username & hashtag, mode tema terang/gelap, progres scraping, dan pesan error jika diblokir.
