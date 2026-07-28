# Track Spec: Application Finalization, UI Color Harmony & Deployment Preparation

## Goal
Melakukan finalisasi penuh pada aplikasi agar siap di-deploy, menyelaraskan skema warna seluruh komponen UI agar senada & harmonis (Theme Emerald SaaS), serta memperbarui form input agar menggunakan placeholder murni.

## Scope & Requirements
1. **Harmonisasi Skema Warna UI (Harmonious Palette)**:
   - Menyeleraskan seluruh warna ikon, tombol, badge, kartu, dan filter menggunakan palet Emerald SaaS (`#10b981` / `#059669` / `#0f172a`) agar tampilan konsisten, senada, dan mahal. Menghapus warna aksen yang bentrok/berbeda-beda.
2. **Form Input Scrape Bersih**:
   - Menghapus nilai default `@eloegelo` di `ScrapePanel.jsx` sehingga input awal tampil kosong dengan placeholder deskripsi: `"Masukkan @username, #hashtag, atau URL postingan..."`.
3. **Pembersihan Repositori**:
   - Menghapus skrip pengujian & file temporary (`debug_graphql.py`, `test_*.py`, `graphql_sample.json`) di folder backend.
4. **Dokumentasi & Production Build Verification**:
   - Membuat `README.md` panduan instalasi/deployment dan memverifikasi build produksi frontend (`dist/`).
