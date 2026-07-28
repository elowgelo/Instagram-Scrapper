import re
from typing import List
from models import InstagramPost, FilterRequest

def filter_posts(posts: List[InstagramPost], req: FilterRequest) -> List[InstagramPost]:
    if not posts:
        return []
        
    # Standardize keywords: trim and lowercase
    keywords = [k.strip().lower() for k in req.keywords if k.strip()]
    target_username = req.target_username.strip().lower().replace("@", "") if req.target_username else None
    match_mode = req.match_mode.upper() if req.match_mode else "OR"

    filtered = []

    for post in posts:
        # Username Filter check
        if target_username and target_username not in post.username.lower():
            continue

        # If no keywords supplied, include post
        if not keywords:
            post_copy = post.model_copy()
            post_copy.matched_keywords = []
            filtered.append(post_copy)
            continue

        caption_lower = post.caption.lower()
        matched = []

        if match_mode == "REGEX":
            for pattern in keywords:
                try:
                    if re.search(pattern, post.caption, re.IGNORECASE):
                        matched.append(pattern)
                except Exception:
                    pass
            is_match = len(matched) > 0
        elif match_mode == "AND":
            # ALL keywords must exist as substring in caption
            matched = [k for k in keywords if k in caption_lower]
            is_match = len(matched) == len(keywords)
        elif match_mode == "EXACT":
            # Exact whole-word match
            for k in keywords:
                if re.search(rf"\b{re.escape(k)}\b", caption_lower):
                    matched.append(k)
            is_match = len(matched) > 0
        else:
            # Default "OR": Substring or numeric matching (matches "ra" inside "ramadhan", "2026" in "2026", etc.)
            matched = [k for k in keywords if k in caption_lower]
            is_match = len(matched) > 0

        if is_match:
            post_copy = post.model_copy()
            post_copy.matched_keywords = matched
            filtered.append(post_copy)

    return filtered
