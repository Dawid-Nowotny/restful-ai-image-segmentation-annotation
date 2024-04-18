from fastapi import FastAPI
from image import router as image_router

app = FastAPI()

app.include_router(image_router.router, prefix="/images", tags=["image"])

@app.get("/")
async def root():
    return {"message": "Hello` World"}