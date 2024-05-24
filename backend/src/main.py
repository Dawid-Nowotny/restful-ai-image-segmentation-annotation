from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from image import router as image_router
from user import router as user_router
from admin import router as admin_router

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router.router, prefix="/images", tags=["Image"])
app.include_router(user_router.router, prefix="/user", tags=["User"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])