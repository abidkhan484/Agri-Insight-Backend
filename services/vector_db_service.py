from config.database import SessionLocal
from models.youtube_transcripts import YoutubeTranscript
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
    
    db = SessionLocal()
    try:
        for idx, chunk in enumerate(chunks):
            try:
                vector = embeddings.embed_documents([chunk])[0]
                transcript_entry = YoutubeTranscript(
                    video_id=video_id,
                    title=title,
                    chunk_index=idx,
                    chunk_text=chunk,
                    embedding=vector
                )
                db.add(transcript_entry)
                log.info("Stored chunk", extra={"extra": {"video_id": video_id, "chunk_index": idx}})
            except Exception as e:
                log.error("Failed to store chunk", extra={"extra": {"video_id": video_id, "chunk_index": idx, "error": str(e)}})
                db.rollback()
                return False
        db.commit()
        return True
    except Exception as e:
        log.error("Failed to store transcript", extra={"extra": {"video_id": video_id, "error": str(e)}})
        db.rollback()
        return False
    finally:
        db.close()

async def query_transcripts(query: str, top_k: int = 3):
    query_vector = embeddings.embed_query(query)
    db = SessionLocal()
    try:
        # Use raw SQL with text() for pgvector operators
        from sqlalchemy import text
        
        result = db.execute(
            text("""
            SELECT 
                id,
                video_id,
                title,
                chunk_index,
                chunk_text,
                1 - (embedding <=> :query_vector::vector) AS similarity
            FROM youtube_transcripts
            ORDER BY embedding <=> :query_vector::vector
            LIMIT :top_k
            """),
            {"query_vector": query_vector, "top_k": top_k}
        ).fetchall()
        
        return [
            {
                "id": row.id,
                "video_id": row.video_id,
                "title": row.title,
                "chunk_index": row.chunk_index,
                "chunk_text": row.chunk_text,
                "similarity": row.similarity
            }
            for row in result
        ]
    finally:
        db.close()
