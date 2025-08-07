import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from api.v1.api import api_router
from config.logger import get_logger

# Set up logging to file only (disable console/stdout handlers)
logger = get_logger("agri-insight")
logging.root.handlers = []  # Remove root handlers
logging.root.addHandler(logger.handlers[0])
logging.root.setLevel(logging.INFO)

# Remove uvicorn's default handlers (stdout)
for uvicorn_logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    uvicorn_logger = logging.getLogger(uvicorn_logger_name)
    uvicorn_logger.handlers = []
    uvicorn_logger.propagate = True

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
