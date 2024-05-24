from fastapi import HTTPException

from models import User

class AdminServices:
    def check_if_admin(self, user):
        if user.role != "Admin":
            raise HTTPException(status_code=403, detail="Tylko administrator może nadać rolę moderatora")
        
    def get_moderators(self, db):
        moderators = db.query(User).filter(User.role == "Moderator").all()
        return moderators
        
    def make_moderator(self, username, db):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="Użytkownik nie został znaleziony")

        if user.role == "Moderator":
            raise HTTPException(status_code=400, detail="Użytkownik jest już moderatorem")

        user.role = "Moderator"
        db.add(user)
        db.commit()
        db.refresh(user)