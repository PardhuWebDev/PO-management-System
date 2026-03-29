import google.generativeai as genai
from pymongo import MongoClient
from datetime import datetime
from app.config import settings

# Gemini setup
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# MongoDB setup
mongo_client = MongoClient(settings.MONGO_URL)
mongo_db     = mongo_client["po_management"]
logs_col     = mongo_db["ai_description_logs"]


def generate_product_description(name: str, category: str) -> str:
    prompt = (
        f"Write a professional 2-sentence marketing description for a product called "
        f'"{name}" in the "{category}" category. '
        f"Make it concise, compelling, and suitable for a B2B purchase order system. "
        f"Return only the description, no extra text."
    )

    description = None
    error        = None

    try:
        response    = model.generate_content(prompt)
        description = response.text.strip()
    except Exception as e:
        error       = str(e)
        description = (
            f"The {name} is a premium {category} product designed for professional use. "
            f"It delivers exceptional quality and reliability for your business needs."
        )

    try:
        logs_col.insert_one({
            "timestamp":    datetime.utcnow(),
            "product_name": name,
            "category":     category,
            "prompt":       prompt,
            "description":  description,
            "model":        "gemini-1.5-flash",
            "error":        error,
            "source":       "gemini-api" if not error else "fallback"
        })
    except Exception:
        pass

    return description


def get_description_logs(limit: int = 50) -> list:
    try:
        logs = list(
            logs_col.find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )
        for log in logs:
            if "timestamp" in log:
                log["timestamp"] = log["timestamp"].isoformat()
        return logs
    except Exception:
        return []
