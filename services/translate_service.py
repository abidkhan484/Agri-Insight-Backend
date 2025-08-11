import os
import httpx
from dotenv import load_dotenv
from config.logger import log

load_dotenv()
TRANSLATE_API_KEY = os.getenv("TRANSLATE_API_KEY")
TRANSLATE_API_ENDPOINT = os.getenv("TRANSLATE_API_ENDPOINT")

async def translate_transcript(raw_transcript: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TRANSLATE_API_ENDPOINT, json={
                "q": raw_transcript,
                "source": "auto",
                "target": "en",
                "format": "text",
                "alternatives": 3,
                "api_key": TRANSLATE_API_KEY,
            }, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data.get("translatedText", None)
    except Exception as e:
        log.error(e, exc_info=True)
