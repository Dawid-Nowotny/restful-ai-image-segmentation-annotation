from fastapi import APIRouter, UploadFile, File, Body, Form, Depends
from typing import Annotated
from .services import UserServices
from .schemas import ImageData

router = APIRouter()

@router.post("/upload")
async def upload(image_data: ImageData = Depends(), file: UploadFile = File(...)):
  userServices = UserServices()
  userServices.add_image_to_database(image_data, file)
  return {
    "saved_image": file.filename
  }

  