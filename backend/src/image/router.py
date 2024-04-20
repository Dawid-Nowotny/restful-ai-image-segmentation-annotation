from fastapi import APIRouter, UploadFile, File, Body, Form, Depends
from typing import Annotated
from .services import UserServices
from .schemas import ImageData

router = APIRouter()

@router.post("/upload")
async def upload(imageData: ImageData = Depends(), file: UploadFile = File(...)):
  #print(ImageSchema)
  #print(image.filename)
  userServices = UserServices()
  userServices.updateImage()
  return {
    "JSON Payload": {"name": "bebe"},
    "Filename": file.filename
  }

  