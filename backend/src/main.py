from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_csrf import CSRFMiddleware

from image import router as image_router
from user import router as user_router
from admin import router as admin_router
from statistics import router as statistics_router

from config import CSRF_SECRET

app = FastAPI(root_path='/api')

app.add_middleware(CSRFMiddleware, secret=CSRF_SECRET, cookie_samesite="strict", cookie_secure=True)

app.include_router(image_router.router, prefix="/images", tags=["Image"])
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(statistics_router.router, prefix="/statistics", tags=["Statistics"])