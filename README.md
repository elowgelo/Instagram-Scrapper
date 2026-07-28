# 📸 Instagram Scraper & Keyword Filter Engine (SaaS Edition)

A high-performance, automated Instagram Web Scraping and Real-time Keyword Filtering Engine built with **FastAPI**, **Playwright Chromium**, **SQLite**, and **React + Vite**.

![Emerald SaaS Theme](https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&auto=format&fit=crop)

---

## 🌟 Key Features

- **🤖 Automated Live Web Scraping**: Scrapes posts, captions, images, and metadata directly using headless Playwright Chromium (supports `@username`, `#hashtag`, and Post URLs).
- **👤 Real Instagram Author & Profile Picture Extraction**: Extracts the actual post owner's handle (`@username`) and Profile Picture (PP) directly from Instagram GraphQL payloads.
- **❤️ Exact Likes & Comments Engagement Parsing**: Captures real engagement metrics directly from Instagram post metadata.
- **🔍 Substring & Numeric Keyword Filter Engine**: Search and highlight exact or partial text substrings (e.g., `"ra"` matches `"ramadhan"`) as well as numeric strings (e.g., `"2026"`). Supports `OR`, `AND`, `EXACT`, and `REGEX` modes.
- **📊 Analytics Sorting**: Sort filtered posts instantly by **Newest**, **Most Likes**, or **Most Comments**.
- **📋 1-Click Copy Caption**: Copy post captions instantly with feedback toast.
- **🚀 Deep Infinite Scroll (Unlimited Mode)**: Option to fetch all available posts by scrolling deep into Instagram search grids (`max_posts = 0`).
- **⚡ Execution Pipeline Stepper**: Live visual timeline feedback during scraping with active status indicators (Yellow = Running, Green = Completed, Red = Error).
- **🎨 Emerald SaaS Professional UI**: Clean, expensive-looking Dark/Light glassmorphism theme built with Vanilla CSS variables and Lucide icons.
- **📥 CSV & JSON Export**: Export filtered dataset with 1-click.

---

## 🌐 Panduan Deploy Gratis 100% (Free Hosting Guide)

Aplikasi ini menggunakan arsitektur terpisah (**Frontend React** dan **Backend FastAPI + Playwright**). Keduanya bisa di-deploy secara **100% GRATIS**!

### Langkah 1: Push Project ke GitHub
1. Buat repository baru di [GitHub](https://github.com/new) (misal: `instagram-scraper-app`).
2. Push seluruh folder project ke GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/instagram-scraper-app.git
   git push -u origin main
   ```

---

### Langkah 2: Deploy Backend FastAPI + Playwright (GRATIS di Render / Koyeb)

Karena backend menggunakan **Playwright Chromium**, kita dianjurkan menggunakan fitur **Docker Deployment** gratis di **Render.com** atau **Koyeb.com**.

#### Option A: Render.com (Rekomendasi)
1. Daftar / Login ke [Render.com](https://render.com/).
2. Klik **New +** &rarr; pilih **Web Service**.
3. Hubungkan repository GitHub `instagram-scraper-app` Anda.
4. Pilih **Language**: `Docker` (Render otomatis mendeteksi file `backend/Dockerfile`).
5. Pada **Root Directory**, isi: `backend`.
6. Pilih **Free Plan** (`$0/month`).
7. Klik **Create Web Service**.
8. Setelah deployment selesai, Render akan memberikan URL Backend Publik (contoh: `https://ig-scraper-api.onrender.com`).

---

### Langkah 3: Deploy Frontend React (GRATIS di Vercel / Netlify)

#### Option A: Vercel (Rekomendasi)
1. Daftar / Login ke [Vercel.com](https://vercel.com/).
2. Klik **Add New...** &rarr; **Project**.
3. Import repository GitHub `instagram-scraper-app`.
4. Pada **Framework Preset**, pilih **Vite**.
5. Pada **Root Directory**, isi: `frontend`.
6. Buka bagian **Environment Variables**:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: URL backend Render Anda (contoh: `https://ig-scraper-api.onrender.com`)
7. Klik **Deploy**.
8. Dalam beberapa detik, Vercel akan memberikan URL web aplikasi siap pakai (contoh: `https://instagram-scraper-app.vercel.app`).

---

## 🚀 Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📝 License
Distributed under the MIT License. Built with ❤️ for automated web scraping and content analytics.
