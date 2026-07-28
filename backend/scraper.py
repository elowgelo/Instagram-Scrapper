import os
import urllib.parse
import requests
from typing import List
from models import InstagramPost, ScrapeRequest
from playwright_scraper import scrape_instagram_with_playwright, extract_posts_from_instagram_json

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
    is_hashtag = target.startswith("#")
    raw_session = request.session_id or os.getenv("INSTAGRAM_SESSION_ID")
    is_unlimited = (request.max_posts == 0)
    target_limit = 999999 if is_unlimited else request.max_posts

    # If Unlimited Mode (max_posts == 0) or High Limit (> 64), run Playwright Deep Infinite Scroll FIRST to fetch 1000+ posts!
    if is_unlimited or request.max_posts > 64:
        print(f"[SCRAPER] High Limit / Unlimited Mode requested ({request.max_posts}). Launching Playwright Deep Infinite Scroll...", flush=True)
        try:
            pw_posts = scrape_instagram_with_playwright(target, request.max_posts, raw_session)
            if pw_posts and len(pw_posts) > 64:
                print(f"[SCRAPER] Playwright Deep Scroll SUCCESS: Got {len(pw_posts)} REAL posts!", flush=True)
                return pw_posts
        except Exception as e:
            print(f"[SCRAPER] Playwright strategy note: {e}", flush=True)

    # Strategy: Direct Instagram REST API (Lightning Fast for Standard Limits <= 64)
    parsed_cookies = parse_cookie_header(raw_session)
    if parsed_cookies:
        try:
            csrf_token = parsed_cookies.get("csrftoken", "")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "X-IG-App-ID": "936619743392459",
                "X-CSRFToken": csrf_token,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"https://www.instagram.com/{clean_target}/"
            }

            if is_hashtag:
                url = f"https://www.instagram.com/api/v1/tags/web_info/?tag_name={clean_target}"
            else:
                url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={clean_target}"

            print(f"[SCRAPER] Trying Direct Instagram REST API (CSRF={bool(csrf_token)}): {url}", flush=True)
            resp = requests.get(url, headers=headers, cookies=parsed_cookies, allow_redirects=False, timeout=8)
            
            if resp.status_code == 200:
                json_data = resp.json()
                api_posts = extract_posts_from_instagram_json(json_data, clean_target)
                if api_posts:
                    print(f"[SCRAPER] Direct Instagram REST API SUCCESS: Extracted {len(api_posts)} REAL posts!", flush=True)
                    return api_posts[:target_limit]
            elif resp.status_code in (301, 302, 307, 308):
                print(f"[SCRAPER] Direct REST API redirected ({resp.status_code}) -> Instagram session cookie missing or invalid.", flush=True)
        except Exception as e:
            print(f"[SCRAPER] Direct REST API note: {e}", flush=True)

    # Strategy Fallback: Playwright Browser Scraper
    try:
        pw_posts = scrape_instagram_with_playwright(target, request.max_posts, raw_session)
        if pw_posts:
            print(f"[SCRAPER] Playwright Browser Scraper SUCCESS: Got {len(pw_posts)} REAL posts!", flush=True)
            return pw_posts
    except Exception as e:
        print(f"[SCRAPER] Playwright strategy note: {e}", flush=True)

    return []
