from fastapi import UploadFile, File, HTTPException, status
from typing import IO
from sqlalchemy import insert
from datetime import date
from models import Image
from database import engine
from .schemas import ImageData
import filetype

class UserServices:
  def add_image_to_database(self, image_data: ImageData, image: UploadFile = File(...)):

    stmt = (
      insert(Image).
      values(
        image = image.file.read(),
        segmented_image = bytes("TMP_SEGMENTED_IMAGE", "utf-8"),
        coordintes_classes = {"TMP_COORDS": "XYZ"},
        upload_date = date.today(),
        uploader_id = image_data.uploader_id,
        moderator_id = image_data.moderator_id
        )
    )

    with engine.connect() as conn:
      conn.execute(stmt)
      conn.commit()

  def validate_file_size_type(self, file: IO):
    FILE_SIZE = 2097152 # 5MB
    accepted_file_types = ["image/png", "image/jpeg", "image/jpg", "png", "jpeg", "jpg"] 

    file_info = filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type",
        )

    detected_content_type = file_info.extension.lower()

    if (
        file.content_type not in accepted_file_types
        or detected_content_type not in accepted_file_types
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large")
