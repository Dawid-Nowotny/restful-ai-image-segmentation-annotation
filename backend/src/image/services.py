from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy import insert, exc
from sqlalchemy.orm import Session
import filetype
from PIL import Image as PILImage

from datetime import date
from typing import IO
from io import BytesIO

from models import Image
from database import engine
from .schemas import ImageData

class ImageServices:
   def get_image_BLOB_by_id(self, image_id: int, db: Session) -> bytes:
      image_blob = db.query(Image.image).filter(Image.id == image_id).first()

      if not image_blob:
          raise HTTPException(status_code=404, detail="Image not found")
      return image_blob[0]

   def BLOB_to_image(self, image_blob) -> PILImage.Image:
      return PILImage.open(BytesIO(image_blob))

class UserServices:
  def add_image_to_database(self, image_data: ImageData, image: UploadFile = File(...)) -> None:
    stmt = (
      insert(Image).
      values(
        image = image.file.read(),
        segmented_image = bytes("TMP_SEGMENTED_IMAGE", "utf-8"),
        coordinates_classes = {"TMP_COORDS": "XYZ"},
        upload_date = date.today(),
        uploader_id = image_data.uploader_id,
        moderator_id = image_data.moderator_id
        )
    )

    try:
      with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
    except exc.SQLAlchemyError as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = e._message())

  def validate_file_size_type(self, file: IO) -> None:
    FILE_SIZE = 5 * 1024 * 1024 # 5MB
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
            raise HTTPException(
              status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
              detail="Uploaded file is too large. Limit is 5MB"
            )