from sqlalchemy import insert
from datetime import date
from models import Image
from database import engine



class UserServices:
  def updateImage(self):
    stmt = (
      insert(Image).
      values(
        image = bytes("1010", "utf-8"),
        segmented_image = bytes("1010", "utf-8"),
        coordintes_classes = {"message": "PICTURE"},
        upload_date = date.today(),
        uploader_id = 0,
        moderator_id = 0
        )
    )

    with engine.connect() as conn:
      conn.execute(stmt)
      conn.commit()
    
    #put image into database
    #stmt = insert(Image).values(uploader)