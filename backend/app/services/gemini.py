import google.generativeai as genai
from app.config import settings

# Configure Gemini client once at import time
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # free tier model


def generate_product_description(name: str, category: str) -> str:
    """
    Given a product name and category, ask Gemini to write
    a professional 2-sentence marketing description.
    Falls back to a template if the API call fails.
    """
    prompt = (
        f"Write a professional 2-sentence marketing description for a product called "
        f'"{name}" in the "{category}" category. '
        f"Make it concise, compelling, and suitable for a B2B purchase order system. "
        f"Return only the description, no extra text."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Graceful fallback — never crash the API over a description
        return (
            f"The {name} is a premium {category} product designed for professional use. "
            f"It delivers exceptional quality and reliability for your business needs."
        )