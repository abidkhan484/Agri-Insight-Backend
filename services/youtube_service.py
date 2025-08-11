import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from services.translate_service import translate_transcript
from dotenv import load_dotenv
from config.logger import log

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

async def get_video_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'hi', 'bn'])
        raw_transcript = " ".join([entry["text"] for entry in transcript.to_raw_data()])
        # If not English, translate
        if hasattr(transcript, 'language_code') and transcript.language_code != 'en':
            raw_transcript = await translate_transcript(raw_transcript)
        return raw_transcript
    except Exception as e:
        log.error(e, exc_info=True)
        return None