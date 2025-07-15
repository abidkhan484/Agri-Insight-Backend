from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, ARRAY, Float

Base = declarative_base()

class Vector(TypeDecorator):
    impl = ARRAY(Float)
    cache_ok = True
    def __init__(self, dimensions, **kwargs):
        super().__init__(Float, **kwargs)
        self.dimensions = dimensions
    def process_bind_param(self, value, dialect):
        return value
    def process_result_value(self, value, dialect):
        return value

class YoutubeTranscript(Base):
    __tablename__ = "youtube_transcripts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    video_id = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    transcript = Column(Text)
    embedding = Column(Vector(384))  # 384 dims for MiniLM-L6-v2 