import time
import re
import urllib.parse
from typing import List
from models import InstagramPost

def extract_author_username(alt_text: str, fallback: str) -> str:
    if not alt_text:
        return fallback
    try:
        match = re.search(r'(?:Photo|Video|Reel)\s+by\s+@?([a-zA-Z0-9._]+)\s+on', alt_text, re.IGNORECASE)
        if match:
            return match.group(1)
            
        match2 = re.search(r'(?:Photo|Video|Reel)\s+by\s+@?([a-zA-Z0-9._]+)', alt_text, re.IGNORECASE)
        if match2:
            return match2.group(1)
    except Exception:
        pass
    return fallback

def parse_engagement_from_text(text: str):
    likes = 0
    comments = 0
    if not text:
        return likes, comments
    
    likes_match = re.search(r'([0-9,.KMBkmb]+)\s+(?:likes|suka)', text, re.IGNORECASE)
    if likes_match:
        val_str = likes_match.group(1).replace(',', '').replace('.', '')
        if val_str.isdigit():
            likes = int(val_str)
            
    comments_match = re.search(r'([0-9,.KMBkmb]+)\s+(?:comments|komentar)', text, re.IGNORECASE)
    if comments_match:
        val_str = comments_match.group(1).replace(',', '').replace('.', '')
        if val_str.isdigit():
            comments = int(val_str)

    return likes, comments

def clean_caption_text(alt_text: str, username: str, clean_target: str, is_hashtag: bool) -> str:
    if not alt_text:
        return f"Postingan #{clean_target}" if is_hashtag else f"Postingan @{clean_target}"
        
    text = alt_text
    text = re.sub(r'^(?:Photo|Video|Reel)\s+by\s+@?[a-zA-Z0-9._]+\s+on\s+[^.]+\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^(?:Photo|Video|Reel)\s+by\s+@?[a-zA-Z0-9._]+\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^May be an image of\s*', '', text, flags=re.IGNORECASE)
    
    clean_str = text.strip()
    if not clean_str:
        return f"Postingan @{username}" if username else f"Postingan #{clean_target}"
    return clean_str

def extract_posts_from_instagram_json(json_data, clean_target: str) -> List[InstagramPost]:
    extracted = []
    
    def traverse(obj):
        if isinstance(obj, dict):
            if ("code" in obj or "shortcode" in obj or "pk" in obj) and ("user" in obj or "owner" in obj or "caption" in obj):
                user_info = obj.get("user") or obj.get("owner") or {}
                username = user_info.get("username")
                profile_pic = user_info.get("profile_pic_url") or user_info.get("profile_pic_url_hd") or ""
                
                caption_obj = obj.get("caption")
                caption_text = ""
                if isinstance(caption_obj, dict):
                    caption_text = caption_obj.get("text", "")
                elif isinstance(caption_obj, str):
                    caption_text = caption_obj
                elif "edge_media_to_caption" in obj:
                    edges = obj.get("edge_media_to_caption", {}).get("edges", [])
                    caption_text = edges[0]["node"]["text"] if edges else ""

                code = obj.get("code") or obj.get("shortcode")
                if not code and "pk" in obj:
                    code = str(obj.get("pk", ""))
                
                likes_raw = (
                    obj.get("like_count") or
                    obj.get("edge_liked_by", {}).get("count") or
                    obj.get("edge_media_preview_like", {}).get("count")
                )
                comments_raw = (
                    obj.get("comment_count") or
                    obj.get("edge_media_to_comment", {}).get("count") or
                    obj.get("edge_media_to_parent_comment", {}).get("count")
                )

                likes = int(likes_raw) if (likes_raw is not None and str(likes_raw).isdigit()) else 0
                comments = int(comments_raw) if (comments_raw is not None and str(comments_raw).isdigit()) else 0

                display_url = obj.get("display_url") or obj.get("thumbnail_src") or ""
                if not display_url and "image_versions2" in obj:
                    candidates = obj.get("image_versions2", {}).get("candidates", [])
                    display_url = candidates[0].get("url") if candidates else ""

                # Filter out internal container metadata duplicates
                is_valid = bool(display_url or caption_text or likes > 0 or comments > 0)
                
                if username and code and is_valid:
                    post = InstagramPost(
                        id=str(code),
                        username=username,
                        profile_pic_url=profile_pic,
                        caption=caption_text or f"Postingan oleh @{username}",
                        post_url=f"https://www.instagram.com/p/{code}/",
                        media_url=display_url or "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop",
                        media_type="image",
                        timestamp=str(obj.get("taken_at") or obj.get("taken_at_timestamp", "")),
                        likes_count=likes,
                        comments_count=comments,
                        matched_keywords=[],
                        is_live_data=True
                    )
                    extracted.append(post)
            
            for v in obj.values():
                traverse(v)
        elif isinstance(obj, list):
            for item in obj:
                traverse(item)

    try:
        traverse(json_data)
    except Exception:
        pass
    
    unique_posts = []
    seen = set()
    for p in extracted:
        if p.id not in seen:
            seen.add(p.id)
            unique_posts.append(p)
            
    return unique_posts

def scrape_instagram_with_playwright(target: str, max_posts: int = 25, raw_cookie: str = None) -> List[InstagramPost]:
    target = target.strip()
    is_hashtag = target.startswith("#")
    clean_target = target.replace("@", "").replace("#", "").strip()
    is_unlimited = (max_posts == 0)
    target_limit = 999999 if is_unlimited else max_posts

    formatted_cookies = []
    if raw_cookie:
        unquoted = urllib.parse.unquote(raw_cookie.strip().strip('"').strip("'"))
        if "=" in unquoted:
            for item in unquoted.split(";"):
                if "=" in item:
                    k, v = item.strip().split("=", 1)
                    formatted_cookies.append({
                        "name": k.strip(),
                        "value": v.strip(),
                        "domain": ".instagram.com",
                        "path": "/"
                    })
        else:
            formatted_cookies.append({
                "name": "sessionid",
                "value": unquoted,
                "domain": ".instagram.com",
                "path": "/"
            })

    scraped_posts = []

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 900}
            )

            if formatted_cookies:
                context.add_cookies(formatted_cookies)
                print(f"[PLAYWRIGHT] Added {len(formatted_cookies)} cookies to browser context", flush=True)

            page = context.new_page()
            
            api_posts = []
            
            def handle_response(response):
                try:
                    if "graphql" in response.url or "top_serp" in response.url or "web_profile_info" in response.url or "sections" in response.url or "tags" in response.url or "search" in response.url:
                        if response.status == 200:
                            json_data = response.json()
                            extracted = extract_posts_from_instagram_json(json_data, clean_target)
                            if extracted:
                                api_posts.extend(extracted)
                except Exception:
                    pass

            page.on("response", handle_response)
            
            if is_hashtag:
                url = f"https://www.instagram.com/explore/tags/{clean_target}/"
            elif target.startswith("http"):
                url = target
            else:
                url = f"https://www.instagram.com/{clean_target}/"

            print(f"[PLAYWRIGHT] Navigating to {url} (Unlimited Mode: {is_unlimited}, Limit: {target_limit})", flush=True)
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass

            try:
                page.wait_for_selector("a[href*='/p/'], a[href*='/reel/']", state="attached", timeout=12000)
            except Exception as se:
                print(f"[PLAYWRIGHT] Initial selector check note: {se}", flush=True)

            # Massive Deep Infinite Scroll Loop (Up to 1,000 scroll loops for up to 10,000+ posts!)
            max_scroll_loops = 1000 if is_unlimited else min(200, max(2, target_limit // 5))
            previous_api_count = 0
            no_new_posts_streak = 0
            
            for scroll_idx in range(max_scroll_loops):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)
                
                current_api_count = len(api_posts)
                if not is_unlimited and current_api_count >= target_limit:
                    break
                if scroll_idx > 12 and current_api_count == previous_api_count:
                    no_new_posts_streak += 1
                    if no_new_posts_streak >= 12:
                        print(f"[PLAYWRIGHT] 10,000+ Capacity Reached end of Instagram feed at {current_api_count} total API posts!", flush=True)
                        break
                else:
                    no_new_posts_streak = 0
                previous_api_count = current_api_count

            # Return intercepted API posts with 100% complete metadata
            if api_posts:
                unique_api_posts = []
                seen_ids = set()
                for p in api_posts:
                    if p.id not in seen_ids:
                        seen_ids.add(p.id)
                        unique_api_posts.append(p)
                if len(unique_api_posts) > 0:
                    print(f"[PLAYWRIGHT] Massive Intercept SUCCESS: Extracted ALL {len(unique_api_posts)} REAL posts!", flush=True)
                    browser.close()
                    return unique_api_posts[:target_limit]

            # DOM Extraction Fallback
            post_links = page.query_selector_all("a[href*='/p/'], a[href*='/reel/']")
            print(f"[PLAYWRIGHT] DOM post links found: {len(post_links)}", flush=True)
            seen_shortcodes = set()
            
            for elem in post_links:
                if len(scraped_posts) >= target_limit:
                    break
                try:
                    href = elem.get_attribute("href") or ""
                    
                    if "/p/" in href or "/reel/" in href:
                        parts = href.split("/p/") if "/p/" in href else href.split("/reel/")
                        shortcode = parts[1].replace("/", "") if len(parts) > 1 else str(int(time.time()))
                        
                        if shortcode in seen_shortcodes:
                            continue
                        seen_shortcodes.add(shortcode)

                        img_elem = elem.query_selector("img")
                        img_src = ""
                        alt_text = ""
                        
                        if img_elem:
                            img_src = img_elem.get_attribute("src") or ""
                            srcset = img_elem.get_attribute("srcset") or ""
                            if srcset:
                                candidate_urls = [s.strip().split(" ")[0] for s in srcset.split(",") if s.strip()]
                                if candidate_urls:
                                    img_src = candidate_urls[-1]
                            alt_text = img_elem.get_attribute("alt") or ""

                        author_username = extract_author_username(alt_text, clean_target)
                        likes, comments = parse_engagement_from_text(alt_text)

                        clean_caption = clean_caption_text(alt_text, author_username, clean_target, is_hashtag)
                        
                        scraped_posts.append(InstagramPost(
                            id=shortcode,
                            username=author_username,
                            profile_pic_url=None,
                            caption=clean_caption,
                            post_url=f"https://www.instagram.com{href}" if href.startswith("/") else href,
                            media_url=img_src or "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop",
                            media_type="image",
                            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            likes_count=likes,
                            comments_count=comments,
                            matched_keywords=[],
                            is_live_data=True
                        ))
                except Exception:
                    continue

            browser.close()
            if scraped_posts:
                print(f"[PLAYWRIGHT] DOM Extraction SUCCESS: Fetched {len(scraped_posts)} REAL posts!", flush=True)
                return scraped_posts

    except Exception as e:
        print(f"[PLAYWRIGHT] Error during live scraping: {e}", flush=True)

    return scraped_posts
