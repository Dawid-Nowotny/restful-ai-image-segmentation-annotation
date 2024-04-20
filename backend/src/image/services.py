from fastapi import UploadFile, File
from sqlalchemy import insert
from datetime import date
from models import Image
from database import engine
from .schemas import ImageData

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
