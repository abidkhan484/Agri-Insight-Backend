import os
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from api.v1.api import api_router

# Load API keys from environment variable (comma-separated)
API_KEYS = os.getenv("API_KEYS", "")
API_KEY_SET = set(key.strip() for key in API_KEYS.split(",") if key.strip())
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key in API_KEY_SET:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

app = FastAPI(
    title="Agri Insight",
    description="API for Agri Insight platform",
    version="1.0.0",
    dependencies=[Depends(get_api_key)]
)

@app.get("/")
def root():
    return {"message": "Agri Insight API is running."}

app.include_router(api_router, prefix="/api/v1")
