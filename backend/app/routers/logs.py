from fastapi import APIRouter
from app.services.gemini import get_description_logs

router = APIRouter()


@router.get("/")
def get_logs(limit: int = 50):
    """
    Returns the last N AI-generated description logs from MongoDB.
    Each log contains the product name, category, prompt, 
    generated description, and timestamp.
    """
    return {
        "count": limit,
        "logs":  get_description_logs(limit)
    }
