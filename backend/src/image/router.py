from fastapi import APIRouter
from .services import UserServices

router = APIRouter()

@router.post("/upload")
async def upload():
  userServices = UserServices()
  userServices.updateImage()
  return {"message": "Image uploaded"}

  