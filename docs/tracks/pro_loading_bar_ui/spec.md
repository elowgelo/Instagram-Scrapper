# Track Spec: Professional Loading UI & Dynamic Progress Bar Improvements

## Goal
Meningkatkan tampilan & interaksi Loading UI saat proses scraping berjalan agar terlihat mahal, profesional, tidak tampak beku (*frozen*), dengan persentase progres dinamis hingga 95% saat finalisasi dan teks deskripsi teknis yang natural.

## Scope & Requirements
1. **Tombol Scrape Interaktif (Anti-Freeze)**:
   - Tombol "Mulai Scrape" dilengkapi dengan animasi glowing border & shimmer pulse & spinner aktif agar tampak responsif dan tidak seperti freeze.
2. **Progres Dinamis Mulus (Maksimal 95% saat in-flight)**:
   - Persentase progres naik secara bertahap (15% -> 40% -> 75% -> 95%) dan bertahan di 95% pada tahap finalisasi backend, lalu berubah 100% hanya saat data telah siap.
3. **Status Deskripsi Teknis Natural (Non-AI Look)**:
   - Menggunakan istilah log sistem SaaS profesional:
     - "Menginisialisasi sesi browser..."
     - "Memuat konten halaman Instagram..."
     - "Mengekstrak postingan, username & statistik..."
     - "Sinkronisasi data ke penyimpanan..."
4. **Desain Visual Expensive SaaS Loading Panel**:
   - Progress bar dengan efek emerald shimmer, counter angka progres real-time, dan tampilan transisi yang mahal & bersih.
