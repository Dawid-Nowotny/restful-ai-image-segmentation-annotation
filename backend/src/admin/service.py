from fastapi import HTTPException
from typing import List

from models import User, Image

class AdminServices:
    def check_if_admin(self, user) -> None:
        if user.role != "Admin":
            raise HTTPException(status_code=403, detail="Dostęp tylko dla administratora")
        
    def get_moderators(self, db) -> List[User]:
        moderators = db.query(User).filter(User.role == "Moderator").all()
        return moderators
        
    def make_moderator(self, username, db) -> None:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Użytkownik nie został znaleziony")

        if user.role == "Moderator":
            raise HTTPException(status_code=400, detail="Użytkownik jest już moderatorem")

        user.role = "Moderator"
        db.add(user)
        db.commit()
        db.refresh(user)

    def assign_moderator_to_image(self, image_id, moderator_username, db) -> None:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Obraz nie został znaleziony")

        moderator = db.query(User).filter(User.username == moderator_username, User.role == "Moderator").first()
        if not moderator:
            raise HTTPException(status_code=404, detail="Moderator nie został znaleziony")

        image.moderator_id = moderator.id
        db.add(image)
        db.commit()
        db.refresh(image)

class ModeratorServices:
    def check_if_admin_or_moderator(self, user) -> None:
        if user.role != "Admin" and user.role != "Moderator":
            raise HTTPException(status_code=403, detail="Dostęp tylko dla administratora lub moderatora")
        
    def check_if_moderator_is_assigned_to_image(self, image, user) -> None:
        if user.id != image.moderator_id and user.role != "Admin":
            raise HTTPException(status_code=403, detail="Nie masz permisji do dodania super-tagów do tego obrazu")