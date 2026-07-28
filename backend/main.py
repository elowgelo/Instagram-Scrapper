import os
import io
import time
import asyncio
import pandas as pd
from typing import List, Optional
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException, Query, Response, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from models import InstagramPost, ScrapeRequest, ImportPostsRequest, FilterRequest, ExportRequest
from scraper import scrape_instagram_posts
from filter_engine import filter_posts
from storage import init_sqlite_db, save_posts_to_db, get_all_posts_from_db, clear_all_posts_in_db

DEMO_IMAGES = [
    "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop"
]

executor = ThreadPoolExecutor(max_workers=4)

def ensure_initial_data():
    init_sqlite_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_initial_data()
    yield

app = FastAPI(title="Instagram Scraper & Keyword Filter API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_initial_data()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Instagram Scraper API Running"}

@app.options("/{full_path:path}")
def options_handler(full_path: str):
    return Response(status_code=200)

@app.delete("/api/posts")
def clear_posts(session_token: Optional[str] = Query(None), x_session_token: Optional[str] = Header(None)):
    token = session_token or x_session_token or "default_session"
    clear_all_posts_in_db(token)
    return {"status": "ok", "message": "Semua data postingan berhasil dihapus"}

@app.post("/api/scrape", response_model=List[InstagramPost])
async def scrape_posts(req: ScrapeRequest):
    if not req.target:
        raise HTTPException(status_code=400, detail="Target username, hashtag, atau URL wajib diisi")
        
    loop = asyncio.get_running_loop()
    posts = await loop.run_in_executor(executor, scrape_instagram_posts, req)
    
    if not posts:
        raise HTTPException(status_code=400, detail="Gagal melakukan scraping postingan. Akses Instagram diblokir atau target tidak ditemukan/tidak memiliki postingan publik.")
        
    token = req.session_token or "default_session"
    save_posts_to_db(posts, token)
    return posts

@app.post("/api/import", response_model=List[InstagramPost])
def import_custom_posts(req: ImportPostsRequest):
    if not req.username or not req.captions:
        raise HTTPException(status_code=400, detail="Username dan caption postingan wajib diisi")
        
    clean_username = req.username.replace("@", "").strip()
    imported_posts = []
    token = req.session_token or "default_session"
    
    for i, caption_text in enumerate(req.captions):
        if not caption_text.strip():
            continue
        post_id = f"custom_{clean_username}_{i+1}_{int(time.time())}"
        img = DEMO_IMAGES[i % len(DEMO_IMAGES)]
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        post = InstagramPost(
            id=post_id,
            username=clean_username,
            caption=caption_text.strip(),
            post_url=f"https://www.instagram.com/{clean_username}/",
            media_url=img,
            media_type="image",
            timestamp=timestamp,
            likes_count=0,
            comments_count=0,
            matched_keywords=[],
            is_live_data=True
        )
        imported_posts.append(post)
        
    if imported_posts:
        save_posts_to_db(imported_posts, token)
        
    return imported_posts

@app.post("/api/filter", response_model=List[InstagramPost])
def filter_scraped_posts(req: FilterRequest):
    token = req.session_token or "default_session"
    posts_to_filter = req.posts if req.posts else get_all_posts_from_db(token)
    filtered = filter_posts(posts_to_filter, req)
    return filtered

@app.get("/api/posts", response_model=List[InstagramPost])
def get_posts(
    keywords: Optional[str] = Query(None, description="Comma separated keywords"),
    match_mode: str = "OR",
    username: Optional[str] = None,
    session_token: Optional[str] = Query(None),
    x_session_token: Optional[str] = Header(None)
):
    token = session_token or x_session_token or "default_session"
    all_posts = get_all_posts_from_db(token)
    
    if keywords or username:
        kw_list = [k.strip() for k in keywords.split(",")] if keywords else []
        req = FilterRequest(
            keywords=kw_list,
            match_mode=match_mode,
            target_username=username,
            posts=all_posts,
            session_token=token
        )
        return filter_posts(all_posts, req)
        
    return all_posts

@app.post("/api/export")
def export_posts(req: ExportRequest):
    if not req.posts:
        raise HTTPException(status_code=400, detail="Tidak ada postingan untuk diekspor")
        
    data = []
    for p in req.posts:
        data.append({
            "ID": p.id,
            "Username": p.username,
            "Caption": p.caption,
            "Matched Keywords": ", ".join(p.matched_keywords),
            "Likes": p.likes_count,
            "Comments": p.comments_count,
            "Post URL": p.post_url,
            "Media URL": p.media_url,
            "Timestamp": p.timestamp
        })
        
    df = pd.DataFrame(data)
    
    if req.format.lower() == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = Response(content=stream.getvalue(), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=instagram_filtered_posts.csv"
        return response
    else:
        json_str = df.to_json(orient="records", indent=2)
        response = Response(content=json_str, media_type="application/json")
        response.headers["Content-Disposition"] = "attachment; filename=instagram_filtered_posts.json"
        return response

# Mount React frontend/dist for single-port Executable App execution
frontend_dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist_dir):
    app.mount("/", StaticFiles(directory=frontend_dist_dir, html=True), name="static")
