from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from image import router as image_router

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    # allow_headers=["*"],
)



app.include_router(image_router.router, prefix="/images", tags=["image"])