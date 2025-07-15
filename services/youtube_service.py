import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_playlist_videos(playlist_id: str):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    items = response.json().get("items", [])
    videos = [
        {
            "videoId": item["snippet"]["resourceId"]["videoId"],
            "title": item["snippet"]["title"]
        }
        for item in items
    ]
    return videos

def get_video_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception:
        return None 