import sqlite3
import json
from typing import List, Optional
from models import InstagramPost

DB_FILE = "instagram_filter.db"

def init_sqlite_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            username TEXT,
            profile_pic_url TEXT,
            caption TEXT,
            post_url TEXT,
            media_url TEXT,
            media_type TEXT,
            timestamp TEXT,
            likes_count INTEGER,
            comments_count INTEGER,
            matched_keywords TEXT,
            session_token TEXT DEFAULT 'default_session',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Migration if table exists without session_token column
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN session_token TEXT DEFAULT 'default_session'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN profile_pic_url TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()

def save_posts_to_db(posts: List[InstagramPost], session_token: str = "default_session"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    token = session_token or "default_session"
    for post in posts:
        # Composite unique post ID per session to prevent cross-session row collisions
        unique_post_id = f"{token}_{post.id}"
        cursor.execute("""
            INSERT OR REPLACE INTO posts 
            (id, username, profile_pic_url, caption, post_url, media_url, media_type, timestamp, likes_count, comments_count, matched_keywords, session_token)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            unique_post_id,
            post.username,
            post.profile_pic_url,
            post.caption,
            post.post_url,
            post.media_url,
            post.media_type,
            post.timestamp,
            post.likes_count,
            post.comments_count,
            json.dumps(post.matched_keywords),
            token
        ))
    conn.commit()
    conn.close()

def get_all_posts_from_db(session_token: str = "default_session") -> List[InstagramPost]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    token = session_token or "default_session"
    cursor.execute(
        "SELECT id, username, profile_pic_url, caption, post_url, media_url, media_type, timestamp, likes_count, comments_count, matched_keywords FROM posts WHERE session_token = ? ORDER BY created_at DESC",
        (token,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    posts = []
    for r in rows:
        # Strip session token prefix from id if present for clean UI display
        raw_id = r[0].split("_", 1)[1] if "_" in r[0] and r[0].startswith(token) else r[0]
        posts.append(InstagramPost(
            id=raw_id,
            username=r[1],
            profile_pic_url=r[2],
            caption=r[3],
            post_url=r[4],
            media_url=r[5],
            media_type=r[6],
            timestamp=r[7],
            likes_count=r[8],
            comments_count=r[9],
            matched_keywords=json.loads(r[10]) if r[10] else []
        ))
    return posts

def clear_all_posts_in_db(session_token: str = "default_session"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    token = session_token or "default_session"
    cursor.execute("DELETE FROM posts WHERE session_token = ?", (token,))
    conn.commit()
    conn.close()
