from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class YoutubeTranscript(Base):
    __tablename__ = "youtube_transcripts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    video_id = Column(String, nullable=False)
    title = Column(Text) 
    chunk_index = Column(BigInteger, nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(384))  # 384 dims for MiniLM-L6-v2
    
    # Note: Index is created in migration file
