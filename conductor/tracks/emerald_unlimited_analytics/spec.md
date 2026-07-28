# Track Spec: Unlimited Scraping, Emerald SaaS UI, Analytics & Substring Filter

## Goal
Menambahkan opsi "Tidak Terbatas", memperbaiki username asli & jumlah Like/Komen, meredesain UI dengan skema warna hijau zamrud (Emerald Professional SaaS) yang mahal & tidak kekanak-kanakan, serta mendukung substring keyword matching (misal "ra" atau "2026" mencocokkan & menyorot potongan kata/angka).

## Scope & Requirements
1. **Opsi Limit "Tidak Terbatas / Unlimited" (Fetch All)**:
   - Dropdown limit: 10, 25, 50, 100, dan **Tidak Terbatas (Semua)**.
2. **Fix Username Penulis Postingan Instagram Asli**:
   - Ekstrak username penulis asli (misal `@cafe_kopi_official`), bukan kata kunci hashtag (`#kopi`).
3. **Fix Likes & Comments Count Extraction**:
   - Tampilkan angka Like & Komentar real yang diekstrak dari DOM / Playwright.
4. **Hapus Fitur Tab "Impor Postingan Saya"**:
   - Hapus tab impor manual agar UI bersih, terfokus, & ringkas.
5. **Redesain UI: Emerald Professional Theme (Less AI Look, Expensive SaaS Vibe)**:
   - Ubah warna tombol dari warna-warni menjadi **Hijau Zamrud Emerald** (`#10b981` / `#059669`).
   - Tampilan bersih, profesional, elegan, dan terstruktur tanpa gradasi norak.
6. **Substring Keyword Matching & Highlighting**:
   - Pencarian kata kunci (misal "ra" atau "2026") akan mencocokkan dan menyorot kata/kalimat/angka yang mengandung substring tersebut.
7. **Fitur Tambahan Analytics & Copy**:
   - Pengurutan postingan (Paling Banyak Like, Komentar, Terbaru) & Tombol Salin Caption 1x klik.
