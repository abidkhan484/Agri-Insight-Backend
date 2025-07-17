from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="Agri Insight",
    description="API for Agri Insight platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Agri Insight API is running."}

app.include_router(api_router, prefix="/api/v1")
