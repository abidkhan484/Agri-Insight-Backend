from config.database import supabase
from langchain.embeddings import HuggingFaceEmbeddings
import re
from config.logger import log

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

sanitize_re = re.compile(r'[^\x00-\x7F]+')
def sanitize_text(text):
    text = sanitize_re.sub(' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

CHUNK_SIZE = 1000
def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

async def store_transcript_vector(
    video_id: str,
    title: str,
    transcript: str,
) -> bool:
    sanitized = sanitize_text(transcript)
    chunks = chunk_text(sanitized)
    log.info("Storing transcript", extra={"extra": {"video_id": video_id, "num_chunks": len(chunks)}})
    for idx, chunk in enumerate(chunks):
        try:
            vector = embeddings.embed_documents([chunk])[0]
            data = {
                "video_id": video_id,
                "title": title,
                "chunk_index": idx,
                "chunk_text": chunk,
                "embedding": vector
            }
            supabase.table("youtube_transcripts").insert(data).execute()
            log.info("Stored chunk", extra={"extra": {"video_id": video_id, "chunk_index": idx}})
        except Exception as e:
            log.error("Failed to store chunk", extra={"extra": {"video_id": video_id, "chunk_index": idx, "error": str(e)}})
            return False
    return True

async def query_transcripts(query: str, top_k: int = 3):
    query_vector = embeddings.embed_query(query)
    response = supabase.rpc(
        "match_youtube_transcripts",
        {"query_embedding": query_vector, "match_count": top_k}
    ).execute()
    return response.data
