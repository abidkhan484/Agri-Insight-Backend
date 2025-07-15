from fastapi import APIRouter, Query
from services.youtube_service import get_playlist_videos, get_video_transcript
from services.vector_db_service import store_transcript_vector
from typing import List

router = APIRouter()

@router.post("/fetch_and_store_transcripts")
def fetch_and_store_transcripts(playlist_id: str = Query(..., description="YouTube Playlist ID")):
    """
    Fetch transcripts for all videos in a playlist, embed them, and store in Supabase vector DB.
    """
    videos = get_playlist_videos(playlist_id)
    results = []
    for video in videos:
        transcript = get_video_transcript(video["videoId"])
        if transcript:
            store_transcript_vector(video["videoId"], video["title"], transcript)
        results.append({"videoId": video["videoId"], "title": video["title"], "transcript": transcript})
    return results
