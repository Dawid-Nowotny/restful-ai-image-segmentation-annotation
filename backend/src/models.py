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

image_likes = Table(
    "ImageLikes",
    Base.metadata,
    Column("image_id", ForeignKey("Image.id",  name="image_likes_image_id"), primary_key=True),
    Column("user_id", ForeignKey("User.id", name="image_likes_user_id"), primary_key=True),
)

comment_likes = Table(
    "CommentLikes",
    Base.metadata,
    Column("comment_id", ForeignKey("Comment.id", name="comment_likes_comment_id"), primary_key=True),
    Column("user_id", ForeignKey("User.id", name="comment_likes_user_id"), primary_key=True),
)

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
    comment_users_likes: Mapped[List["User"]] = relationship(secondary=comment_likes, back_populates="user_comments_likes")
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
    image_users_likes: Mapped[List["User"]] = relationship(secondary=image_likes, back_populates="user_images_likes")

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
    user_comments_likes: Mapped[List["Comment"]] = relationship(secondary=comment_likes, back_populates="comment_users_likes")
    user_images_likes: Mapped[List["Image"]] = relationship(secondary=image_likes, back_populates="image_users_likes")

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)