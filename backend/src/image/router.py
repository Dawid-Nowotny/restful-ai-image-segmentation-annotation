from fastapi import APIRouter, UploadFile, File, Depends, Response
from sqlalchemy.orm import Session

import copy
import json

from .services import UserServices, ImageServices, AiAnnotationServices
from .schemas import ImageData
from get_db import get_db

router = APIRouter()

@router.post("/upload")
def upload(image_data: ImageData = Depends(), file: UploadFile = File(...)):
  userServices = UserServices()
  file_test = copy.deepcopy(file)
  userServices.validate_file_size_type(file_test)
  userServices.add_image_to_database(image_data, file)
  return Response(
        content=json.dumps({"saved_image": file.filename}),
        media_type="application/json",
        status_code=200
    )

@router.get("/suggest-annotations")
def suggest_annotations(image_id: int, db: Session = Depends(get_db)):
  image_services = ImageServices()
  ai_annotation_services = AiAnnotationServices()
  
  image_blob = image_services.get_image_BLOB_by_id(image_id, db)
  image = image_services.BLOB_to_image(image_blob)

  annotations = ai_annotation_services.annotate_image(image)
  return Response(
        content=json.dumps({"annotations": annotations}), 
        media_type="application/json", 
        status_code=200
    )