from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api():
    print("Testing GET / ...")
    res = client.get("/")
    assert res.status_code == 200
    print("Root endpoint OK:", res.json())

    print("\nTesting OPTIONS /api/scrape (CORS preflight) ...")
    res = client.options("/api/scrape")
    assert res.status_code == 200
    print("CORS OPTIONS preflight OK!")

    print("\nTesting GET /api/posts ...")
    res = client.get("/api/posts")
    assert res.status_code == 200
    posts = res.json()
    print(f"Posts count: {len(posts)}")
    assert len(posts) > 0

    print("\nTesting POST /api/filter with keyword 'promo' ...")
    res = client.post("/api/filter", json={
        "keywords": ["promo"],
        "match_mode": "OR",
        "posts": posts
    })
    assert res.status_code == 200
    filtered = res.json()
    print(f"Filtered count for 'promo': {len(filtered)}")

    print("\nTesting POST /api/scrape ...")
    res = client.post("/api/scrape", json={
        "target": "@tech_insider",
        "max_posts": 5,
        "include_demo_data": True
    })
    assert res.status_code == 200
    scraped = res.json()
    print(f"Scraped count: {len(scraped)}")

    print("\nTesting POST /api/export CSV ...")
    res = client.post("/api/export", json={
        "format": "csv",
        "posts": filtered
    })
    assert res.status_code == 200
    assert "Username,Caption" in res.text or "ID,Username" in res.text
    print("CSV Export OK! Sample length:", len(res.text))

    print("\nALL BACKEND API TESTS PASSED EMPIRICALLY!")

if __name__ == "__main__":
    test_api()
