# Initial Concept
Aplikasi berbasis web untuk meng-scrape postingan Instagram dan memfilternya berdasarkan kata kunci pada deskripsi/caption postingan.

# Product Overview
**Instagram Post Scraper & Keyword Filter Web Application** adalah aplikasi berbasis web yang memungkinkan pengguna mengambil (scrape) data postingan Instagram (berdasarkan akun target, hashtag, atau pencarian) dan secara otomatis menyaring (filter) postingan tersebut berdasarkan kata kunci spesifik pada caption/deskripsi postingan.

## Core Features
1. **Instagram Scraping Engine**:
   - Scraping postingan dari profil pengguna (public accounts) atau hashtag target.
   - Ekstraksi detail postingan: Caption, URL Gambar/Video, Jumlah Like, Jumlah Komentar, Tanggal Upload, Username Pemilik, dan Direct Link ke postingan IG.
2. **Keyword Filtering & Search**:
   - Filter real-time maupun batch menggunakan kata kunci (match exact, contains, atau regex).
   - Dukungan multiple keywords (OR/AND logic).
   - Highlight kata kunci yang cocok pada hasil caption.
3. **Interactive Dashboard UI**:
   - Tampilan visual postingan berbentuk Grid / Card Feed & Table View.
   - Statistik ringkas: Jumlah postingan di-scrape, jumlah postingan lolos filter, top keywords matched.
   - Detail view untuk melihat gambar/video dan deskripsi lengkap.
4. **Data Management & Export**:
   - Simpan hasil filter ke database/local storage.
   - Export hasil ke format CSV, JSON, atau XLSX.
   - Filter berdasarkan rentang tanggal postingan.

## Target Audience
- Content Creators & Marketers yang mencari riset tren/kompetitor.
- Researchers & Data Analysts yang memantau topik spesifik di Instagram.
- Pengguna umum yang membutuhkan kliping postingan IG sesuai kata kunci.
