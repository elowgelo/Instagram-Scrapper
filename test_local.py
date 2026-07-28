"""
===================================================================
📸 INSTAGRAM SCRAPER - LOCAL TEST SCRIPT
===================================================================
Gunakan skrip ini untuk menguji fungsi scraping & otentikasi secara
langsung di laptop Anda tanpa bergantung pada server cloud.
"""

import os
import sys
import json

# Add backend folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from models import ScrapeRequest
from scraper import scrape_instagram_posts

# Cookie Instagram default dari pengujian Anda
DEFAULT_COOKIE = "ps_l=1; ps_n=1; ig_did=3932CEFC-9019-4089-B464-DB89E4C7A59E; mid=amf9SgALAAHIsup7LFFFQAiFBq6o; datr=3C9oaguUJlsyvT8X2fdCwq1X; csrftoken=JHwBkTgRMRG6Aw1GvF1O7t8ltuxIxxSX; ds_user_id=43339011844; sessionid=43339011844%3A2btyR5SOuWVZVX%3A7%3AAYiMXzmBayrOQ6Y3EW7tK_nYm-fTwNZ-m58evKbOZA; wd=950x682; rur=PRN%2C17841443315337376%2C1786422599%3A01ff92f992a434762c23ecf50d5050f2c1d3dae70b987750c694a3e1ca4b62afa9303f62"

def main():
    target = input("Masukkan target (@username, #hashtag, atau tekan ENTER untuk '#spinetam2026'): ").strip()
    if not target:
        target = "#spinetam2026"

    max_posts_input = input("Masukkan batas postingan (atau tekan ENTER untuk 10): ").strip()
    max_posts = int(max_posts_input) if max_posts_input.isdigit() else 10

    cookie_input = input("Masukkan Cookie Instagram (atau tekan ENTER untuk cookie default Anda): ").strip()
    session_cookie = cookie_input if cookie_input else DEFAULT_COOKIE

    print("\n-----------------------------------------------------------")
    print(f"🚀 MEMULAI SCAPING LOKAL UNTUK: {target}")
    print(f"📦 Batas Postingan: {max_posts}")
    print("-----------------------------------------------------------\n")

    req = ScrapeRequest(target=target, max_posts=max_posts, session_id=session_cookie)
    posts = scrape_instagram_posts(req)

    print("\n===========================================================")
    print(f"✅ ANGGAN/HASIL SCRAPING LOKAL: {len(posts)} Postingan Ditemukan")
    print("===========================================================")

    for idx, post in enumerate(posts[:5], 1):
        print(f"\n[{idx}] Post ID: {post.id}")
        print(f"    Author   : @{post.username}")
        print(f"    Likes    : {post.likes_count} | Comments: {post.comments_count}")
        print(f"    URL      : {post.post_url}")
        print(f"    Caption  : {post.caption[:80]}...")

    if len(posts) > 5:
        print(f"\n... dan {len(posts) - 5} postingan lainnya.")

if __name__ == "__main__":
    main()
