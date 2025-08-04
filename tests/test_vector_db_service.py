import pytest
from fastapi.testclient import TestClient
from services.vector_db_service import sanitize_text, chunk_text
from main import app

client = TestClient(app)

def test_sanitize_text():
    raw = "Hello\nWorld!\u2014This is a test.\n\t"
    sanitized = sanitize_text(raw)
    assert "\n" not in sanitized
    assert "\t" not in sanitized
    assert "  " not in sanitized
    assert "This is a test." in sanitized

def test_chunk_text():
    text = "a" * 2500
    chunks = chunk_text(text, chunk_size=1000)
    assert len(chunks) == 3
    assert all(len(chunk) <= 1000 for chunk in chunks)

def test_fetch_and_store_transcripts(monkeypatch):
    def mock_get_playlist_videos(playlist_id):
        return [{"videoId": "abc123", "title": "Test Video"}]
    def mock_get_video_transcript(video_id):
        return "This is a test transcript."
    def mock_store_transcript_vector(video_id, title, transcript):
        return None
    monkeypatch.setattr("services.youtube_service.get_playlist_videos", mock_get_playlist_videos)
    monkeypatch.setattr("services.youtube_service.get_video_transcript", mock_get_video_transcript)
    monkeypatch.setattr("services.vector_db_service.store_transcript_vector", mock_store_transcript_vector)
    response = client.post("/api/v1/youtube/fetch_and_store_transcripts?playlist_id=PL123")
    assert response.status_code == 200
    assert response.json()[0]["videoId"] == "abc123"

def test_query_transcripts_api(monkeypatch):
    def mock_query_transcripts(query, top_k=3):
        return [{"chunk_text": "Relevant chunk", "score": 0.99}]
    monkeypatch.setattr("services.vector_db_service.query_transcripts", mock_query_transcripts)
    response = client.post("/api/v1/youtube/query_transcripts", json={"query": "test", "top_k": 1})
    assert response.status_code == 200
    assert response.json()[0]["chunk_text"] == "Relevant chunk" 