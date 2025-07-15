import os
from supabase import create_client, Client
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np
from fastapi import APIRouter, Query, Body

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Initialize LangChain embedding model (Sentence Transformers)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def store_transcript_vector(video_id: str, title: str, transcript: str):
    # Embed transcript
    vector = embeddings.embed_documents([transcript])[0]
    # Store in Supabase (assumes a table 'youtube_transcripts' with columns: video_id, title, transcript, embedding)
    data = {
        "video_id": video_id,
        "title": title,
        "transcript": transcript,
        "embedding": vector
    }
    supabase.table("youtube_transcripts").insert(data).execute()

def query_transcripts(query: str, top_k: int = 3):
    # Embed the query
    query_vector = embeddings.embed_query(query)
    # Query Supabase for the most similar vectors
    response = supabase.rpc(
        "match_youtube_transcripts",  # This is a Postgres function you need to create
        {"query_embedding": query_vector, "match_count": top_k}
    ).execute()
    return response.data

router = APIRouter()

@router.post("/query_transcripts")
def query_transcripts_api(query: str = Body(..., embed=True), top_k: int = 3):
    """
    Query the vector DB for relevant transcript chunks.
    """
    results = query_transcripts(query, top_k=top_k)
    return results 