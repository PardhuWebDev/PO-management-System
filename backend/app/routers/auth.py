from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings
from app import schemas

router = APIRouter()

GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO  = "https://www.googleapis.com/oauth2/v3/userinfo"
REDIRECT_URI     = "http://localhost:8000/auth/callback"


def create_jwt(user_info: dict) -> str:
    payload = {
        "sub":     user_info["email"],
        "name":    user_info.get("name", ""),
        "picture": user_info.get("picture", ""),
        "exp":     datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@router.get("/login")
def login():
    """Redirect user to Google OAuth consent screen"""
    params = (
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    return RedirectResponse(url=GOOGLE_AUTH_URL + params)


@router.get("/callback")
async def auth_callback(code: str):
    """Exchange auth code for tokens, issue JWT, redirect to frontend"""
    async with httpx.AsyncClient() as client:
        # 1. Exchange code for Google access token
        try:
            token_resp = await client.post(GOOGLE_TOKEN_URL, data={
                "code":          code,
                "client_id":     settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri":  REDIRECT_URI,
                "grant_type":    "authorization_code",
            })
            token_resp.raise_for_status()
            google_token = token_resp.json()["access_token"]
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to exchange code with Google")

        # 2. Fetch user info from Google
        try:
            userinfo_resp = await client.get(
                GOOGLE_USERINFO,
                headers={"Authorization": f"Bearer {google_token}"}
            )
            userinfo_resp.raise_for_status()
            user_info = userinfo_resp.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")

    # 3. Create our own JWT
    jwt_token = create_jwt(user_info)

    # 4. Redirect to frontend with token in URL fragment
    frontend_url = f"{settings.FRONTEND_URL}/dashboard.html#token={jwt_token}"
    return RedirectResponse(url=frontend_url)


@router.get("/me", response_model=schemas.UserInfo)
def get_me(token: str):
    """Decode JWT and return user info (used by frontend)"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return schemas.UserInfo(
            email=payload["sub"],
            name=payload.get("name", ""),
            picture=payload.get("picture", "")
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")