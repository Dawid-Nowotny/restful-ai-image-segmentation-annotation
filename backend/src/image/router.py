from fastapi import APIRouter, UploadFile, File, Depends

import copy

from .services import UserServices
from .schemas import ImageData

router = APIRouter()

@router.post("/upload")
def upload(image_data: ImageData = Depends(), file: UploadFile = File(...)):
  userServices = UserServices()
  file_test = copy.deepcopy(file)
  userServices.validate_file_size_type(file_test)
  userServices.add_image_to_database(image_data, file)
  return {
    "saved_image": file.filename
  }

  