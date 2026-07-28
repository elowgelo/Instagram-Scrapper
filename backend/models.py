from pydantic import BaseModel
from typing import List, Optional

class InstagramPost(BaseModel):
    id: str
    username: str
    profile_pic_url: Optional[str] = None
    caption: str
    post_url: str
    media_url: str
    media_type: str = "image"
    timestamp: str
    likes_count: int = 0
    comments_count: int = 0
    matched_keywords: List[str] = []
    is_live_data: bool = True

class ScrapeRequest(BaseModel):
    target: str
    max_posts: int = 20
    session_id: Optional[str] = None

class ImportPostsRequest(BaseModel):
    username: str
    captions: List[str]

class FilterRequest(BaseModel):
    keywords: List[str] = []
    match_mode: str = "OR"
    target_username: Optional[str] = None
    posts: Optional[List[InstagramPost]] = None

class ExportRequest(BaseModel):
    posts: List[InstagramPost]
    format: str = "csv"
