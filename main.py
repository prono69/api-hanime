from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from dateutil import parser
import requests
import json
import secrets

app = FastAPI()

# Global variables for custom fields
CREATOR = "Eyepatch"
API_VERSION = "1.0"

# Utility function to format API responses
def format_response(data, **kwargs):
    return {
        "creator": CREATOR,
        "api_version": API_VERSION,
        **kwargs,
        data,
    }

@app.get("/")
def root(request: Request):
    return format_response({"message": "Welcome to the API"}, hostname=request.url.hostname)

@app.get("/search")
async def search(query: str, page: int):
    payload = {
        "search_text": query,
        "tags": [],
        "brands": [],
        "blacklist": [],
        "order_by": [],
        "ordering": [],
        "page": page,
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post("https://search.htv-services.com", headers=headers, json=payload)
    response_data = response.json()

    return format_response(
        {
            "results": json.loads(response_data["hits"]),
            "page": response_data["page"],
        }
    )

@app.get("/recent")
async def recent(page: int = 0):
    payload = {
        "search_text": "",
        "tags": [],
        "brands": [],
        "blacklist": [],
        "order_by": "created_at_unix",
        "ordering": "desc",
        "page": page,
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post("https://search.htv-services.com", headers=headers, json=payload)
    response_data = response.json()

    return format_response(
        {
            "results": json.loads(response_data["hits"]),
            "page": response_data["page"],
        }
    )

@app.get("/trending")
async def trending(time: str = "month", page: int = 0):
    headers = {
        "X-Signature-Version": "web2",
        "X-Signature": secrets.token_hex(32),
    }
    response = requests.get(
        f"https://hanime.tv/api/v8/browse-trending?time={time}&page={page}",
        headers=headers,
    )
    response_data = response.json()

    return format_response(
        {
            "results": response_data["hentai_videos"],
            "time": response_data["time"],
            "page": response_data["page"],
        }
    )

@app.get("/details")
async def details(id: str):
    response = requests.get(f"https://hanime.tv/api/v8/video?id={id}")
    response_data = response.json()
    video_data = response_data["hentai_video"]

    formatted_data = {
        "query": video_data["slug"],
        "name": video_data["name"],
        "poster": video_data["cover_url"],
        "id": video_data["id"],
        "description": video_data["description"],
        "views": "{:,}".format(video_data["views"]),
        "brand": video_data["brand"],
        "created_at": parser.parse(video_data["created_at"]).strftime("%Y %m %d"),
        "released_date": parser.parse(video_data["released_at"]).strftime("%Y %m %d"),
        "is_censored": video_data["is_censored"],
        "tags": [tag["text"] for tag in video_data["hentai_tags"]],
    }

    return format_response(formatted_data)

@app.get("/link")
async def hentai_video(id: str):
    headers = {
        "X-Session-Token": "PhzIzReFsg7g2GZi-tz9KVpR2LskgMP8-l_xJ0kmbwhSuBOcD3yZJeOoQKS-ND1w3qFCGj0Y2HzfJ4renU82W25BNSVI6KnmwfiN5e9lueyQOYbZ0RVKmS2Ek1fLKvMnS_3ktEUiFOTjSCezPusemw==(-(0)-)hDLS0eC_45mNW15pn3ZJYQ==",
    }
    response = requests.get(f"https://hanime.tv/api/v8/video?id={id}", headers=headers)
    response_data = response.json()

    return format_response(
        {"streams": response_data["videos_manifest"]["servers"][0]["streams"]}
    )

@app.get("/play")
async def play(link: str):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <video id="live" autoplay controls>
            <source src="{link}" type="video/mp4">
        </video>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
    