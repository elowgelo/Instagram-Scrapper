import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import List
from models import InstagramPost, ScrapeRequest
from playwright_scraper import scrape_instagram_with_playwright

def parse_cookie_header(raw_cookie: str) -> dict:
    if not raw_cookie:
        return {}
    
    raw = urllib.parse.unquote(raw_cookie.strip().strip('"').strip("'"))
    cookies = {}
    
    if "=" in raw:
        for part in raw.split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                cookies[k.strip()] = v.strip()
    else:
        cookies["sessionid"] = raw
        ds_user_id = raw.split("%3A")[0].split(":")[0] if ("%3A" in raw or ":" in raw) else ""
        if ds_user_id:
            cookies["ds_user_id"] = ds_user_id
            
    return cookies

def scrape_instagram_posts(request: ScrapeRequest) -> List[InstagramPost]:
    target = request.target.strip()
    clean_target = target.replace("@", "").replace("#", "").strip()
    raw_session = request.session_id or os.getenv("INSTAGRAM_SESSION_ID")

    # Strategy 1: Playwright Chromium Browser Scraper (Supports Username & Hashtags)
    try:
        pw_posts = scrape_instagram_with_playwright(target, request.max_posts, raw_session)
        if pw_posts:
            print(f"[SCRAPER] Playwright Browser Scraper SUCCESS: Got {len(pw_posts)} REAL posts!")
            return pw_posts
    except Exception as e:
        print(f"[SCRAPER] Playwright strategy note: {e}")

    # Strategy 2: Direct Web API Request with Cookie Header
    parsed_cookies = parse_cookie_header(raw_session)
    if parsed_cookies:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "X-IG-App-ID": "936619743392459",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://www.instagram.com/{clean_target}/"
            }

            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={clean_target}"
            resp = requests.get(url, headers=headers, cookies=parsed_cookies, timeout=6)
            
            if resp.status_code == 200:
                data = resp.json()
                user_data = data.get("data", {}).get("user", {})
                timeline = user_data.get("edge_owner_to_timeline_media", {}).get("edges", [])
                
                scraped = []
                for edge in timeline[:request.max_posts]:
                    node = edge.get("node", {})
                    caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                    caption_text = caption_edges[0]["node"]["text"] if caption_edges else ""
                    shortcode = node.get("shortcode") or node.get("id")
                    
                    scraped.append(InstagramPost(
                        id=shortcode,
                        username=user_data.get("username") or clean_target,
                        caption=caption_text,
                        post_url=f"https://www.instagram.com/p/{shortcode}/",
                        media_url=node.get("display_url") or "",
                        media_type="video" if node.get("is_video") else "image",
                        timestamp=str(node.get("taken_at_timestamp", "")),
                        likes_count=node.get("edge_media_preview_like", {}).get("count", 0),
                        comments_count=node.get("edge_media_to_comment", {}).get("count", 0),
                        matched_keywords=[],
                        is_live_data=True
                    ))

                if scraped:
                    return scraped
        except Exception as e:
            print(f"[SCRAPER] Direct Web Profile API error: {e}")

    # No synthetic demo data returned -> Strict failure status if scraping fails or blocked!
    return []
