# Track Spec: Hashtag Scraping Fix, Theme Toggle, & Scraper UI Enhancements

## Goal
Memperbaiki scraping hashtag (`#`), menambahkan 2 mode tema (Gelap & Terang), menghilangkan mode pratinjau sintetis (tampilkan status gagal jika diblokir), menaikkan limit postingan hingga 100, serta menambahkan UI indikator progres scraping dibelakang layar.

## Scope & Requirements
1. **Fix Hashtag (#) Scraping**:
   - Perbaiki pencarian hashtag Instagram di Playwright Chromium (`https://www.instagram.com/explore/tags/<tag>/`).
2. **Dual Theme System (Dark Mode & Light Mode)**:
   - Tombol toggle Sun/Moon di Navbar dengan transisi tema halus (CSS Custom Properties).
3. **Strict Failure Status (No Demo Fallback)**:
   - Hapus generator data pratinjau acak. Jika scraping diblokir/gagal, tampilkan notifikasi error murni tanpa kartu postingan palsu.
4. **Limit Scrape Hingga 100 Postingan**:
   - Opsi pilihan batas: 10, 25, 50, 100 postingan.
5. **Progress Bar / Indicator UI**:
   - Tampilkan indikator status progres real-time saat scraping berjalan.
6. **Code Cleanup**:
   - Hapus sisa kode generator demo acak agar codebase lebih bersih dan terfokus.
