# Implementation Plan: Instagram Scraper & Keyword Filter

## Task List

- [x] Task 1: Setup Proyek & Scaffolding Backend & Frontend
  - Detail: Inisialisasi struktur direktori backend (Python FastAPI) dan frontend (Vite React), buat virtual environment & package manifest (`requirements.txt`, `package.json`).
  - Tech: Python 3.10+, FastAPI, Vite, React, Vanilla CSS.

- [x] Task 2: Implementasi Backend Scraping Engine & Keyword Filtering
  - Detail: Buat module Python scraper (Playwright/Instaloader) untuk mengambil data postingan IG (caption, image URL, username, post link, timestamp, likes/comments) dan engine filter kata kunci.
  - Tech: Playwright/BeautifulSoup, FastAPI API Endpoints (`/api/scrape`, `/api/posts`, `/api/filter`).

- [x] Task 3: Inisialisasi & Desain UI Frontend Dashboard
  - Detail: Buat antarmuka React dengan tema modern dark mode & glassmorphism. Tambahkan form pencarian/scraping, Keyword Filter Bar (input tag kata kunci), serta Toggle Grid/Table Feed View.
  - Tech: React, Vanilla CSS design tokens.

- [x] Task 4: Integrasi Full-Stack & Fitur Export Data
  - Detail: Hubungkan React frontend ke FastAPI backend. Implementasikan tombol ekspor hasil filter ke format CSV dan JSON.
  - Tech: Axios/Fetch API, CSV/JSON exporter.

- [x] Task 5: Pengujian & Empiric Verification
  - Detail: Uji alur scraping, pencocokan kata kunci, penanganan rate limit/error, dan ekspor data secara end-to-end.
