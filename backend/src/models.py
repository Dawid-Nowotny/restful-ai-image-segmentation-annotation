from sqlalchemy import Column, Integer, String, ForeignKey,  JSON, Boolean, Date, LargeBinary, Table, Float
from passlib.context import CryptContext
from sqlalchemy.orm import validates, relationship, Mapped
from validate_email import validate_email as validate_email_format

from typing import List
try:
    from database import Base
except:
    from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Tag(Base):
    __tablename__ = "Tag" 
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tag = Column(String, index=True, nullable=False)

    comment_id = Column(Integer, ForeignKey('Comment.id'))
    comment: Mapped["Comment"] = relationship(back_populates="tags")

class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    super_tag = Column(Boolean, index=True, nullable=False)
    comment_date = Column(Date, index=True, nullable=False)

    image_id = Column(Integer, ForeignKey('Image.id'))
    user_id = Column(Integer, ForeignKey('User.id'))

    image: Mapped["Image"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")
    tags: Mapped[List["Tag"]] = relationship("Tag", back_populates="comment")

class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    image = Column(LargeBinary, nullable=False)
    segmented_image = Column(LargeBinary, nullable=True)
    coordinates_classes = Column(JSON, nullable=True)
    threshold = Column(Float, nullable=False, index=True)
    upload_date = Column(Date, index=True, nullable=False)

    uploader_id = Column(Integer, ForeignKey('User.id'))
    moderator_id = Column(Integer, ForeignKey('User.id'), nullable=True)

    comments: Mapped[List["Comment"]] = relationship(back_populates="image")
    uploader: Mapped["User"] = relationship(back_populates="images", foreign_keys=[uploader_id])
    moderator: Mapped["User"] = relationship(back_populates="images", foreign_keys=[moderator_id])

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, index=True, nullable=False)
    secret_key = Column(String, index=False, nullable=True)

    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    images: Mapped[List["Image"]] = relationship(back_populates="uploader", foreign_keys="[Image.uploader_id]")

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)