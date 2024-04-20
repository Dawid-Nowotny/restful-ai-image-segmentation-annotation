from fastapi import UploadFile, File
from sqlalchemy import insert
from datetime import date
from models import Image
from database import engine
from .schemas import ImageData



class UserServices:
  def updateImage(self, imageData: ImageData, image: UploadFile = File(...)):

    stmt = (
      insert(Image).
      values(
        image = image.file.read(),
        segmented_image = bytes("TMP_SEGMENTED_IMAGE", "utf-8"),
        coordintes_classes = {"TMP_COORDS": "XYZ"},
        upload_date = date.today(),
        uploader_id = imageData.uploader_id,
        moderator_id = imageData.moderator_id
        )
    )

    with engine.connect() as conn:
      conn.execute(stmt)
      conn.commit()