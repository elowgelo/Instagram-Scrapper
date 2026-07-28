# Implementation Plan: Mobile & Smartphone Responsiveness Optimization

## Task List

- [x] Task 1: Tambahkan Media Queries Mobile pada `index.css`
  - Detail: Tambahkan `@media (max-width: 768px)` dan `@media (max-width: 480px)` di `index.css` untuk mengatur navbar, stats grid, input form, feed grid 1-kolom, dan responsive table container.
  - Files: `frontend/src/index.css`.

- [x] Task 2: Penyesuaian Responsif pada Komponen React Navbar & Header
  - Detail: Sesuaikan tata letak komponen `Navbar.jsx`, `StatsHeader.jsx`, dan `ScrapePanel.jsx` agar elemen tombol & input tersusun rapi saat diakses di perangkat seluler.
  - Files: `frontend/src/components/Navbar.jsx`, `frontend/src/components/StatsHeader.jsx`, `frontend/src/components/ScrapePanel.jsx`.

- [x] Task 3: Penyesuaian Responsif pada Feed Kartu & Tabel Hasil Filter
  - Detail: Optimalkan `PostCard.jsx` & `PostTable.jsx` agar teks caption, gambar, statistik like/komen, dan tombol Buka IG mudah dibaca dan di-tap pada layar smartphone.
  - Files: `frontend/src/components/PostCard.jsx`, `frontend/src/components/PostTable.jsx`.

- [x] Task 4: Pengujian & Empiric Verification
  - Detail: Uji kompilasi build produksi `npm run build` dan verifikasi layout responsif di viewport smartphone.
