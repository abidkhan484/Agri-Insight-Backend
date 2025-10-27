from fastapi import APIRouter, Query, Body
from services.youtube_service import get_playlist_videos, get_video_transcript
from services.vector_db_service import store_transcript_vector, query_transcripts
from typing import List

router = APIRouter()

@router.get("/fetch_playlist_transcripts")
async def fetch_playlist_transcripts(playlist_id: str = Query(..., description="YouTube Playlist ID")):
    """
    Fetch transcripts for all videos in a playlist. Does NOT store in DB.
    """
    videos = get_playlist_videos(playlist_id)
    results = []
    for video in videos:
        transcript = await get_video_transcript(video["videoId"])
        results.append({"videoId": video["videoId"], "title": video["title"], "transcript": transcript})
    return results

@router.get("/fetch_video_transcript")
async def fetch_video_transcript(video_id: str = Query(..., description="YouTube Video ID")):
    """
    Fetch transcript for a single video. Does NOT store in DB.
    """
    # TODO: check whether the video id already exists in db
    transcript = await get_video_transcript(video_id)
    return {"videoId": video_id, "transcript": transcript}

@router.post("/store_transcript_vector")
async def store_transcript_vector_api(
    video_id: str = Body(..., embed=True),
    title: str = Body(..., embed=True),
    transcript: str = Body(..., embed=True)
):
    """
    Store transcript in PostgreSQL vector DB after chunking and embedding.
    """
    await store_transcript_vector(video_id, title, transcript)
    return {"status": "success", "videoId": video_id}

@router.post("/query_transcripts")
async def query_transcripts_api(query: str = Body(..., embed=True), top_k: int = 3):
    results = await query_transcripts(query, top_k=top_k)
    return results
