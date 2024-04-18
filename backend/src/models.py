from sqlalchemy import Column, Integer, String, ForeignKey,  JSON, Boolean, Date, LargeBinary, Table
from passlib.context import CryptContext
from sqlalchemy.orm import validates, relationship
from validate_email import validate_email as validate_email_format

from database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

image_likes = Table(
    "ImageLikes",
    Base.metadata,
    Column("Image", ForeignKey("Image.id")),
    Column("User", ForeignKey("User.id")),
)

comment_likes = Table(
    "CommentLikes",
    Base.metadata,
    Column("Comment", ForeignKey("Comment.id")),
    Column("User", ForeignKey("User.id")),
)

class Tag(Base):
    __tablename__ = "Tag"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tag = Column(String, index=True, nullable=False)

    comment = relationship("Comment", backref="Tag")

class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    super_tag = Column(Boolean, index=True, nullable=False)
    comment_date = Column(Date, index=True, nullable=False)

    tag_id = Column(Integer, ForeignKey('Tag.id'))
    user_id = Column(Integer, ForeignKey('User.id'))
    image_id = Column(Integer, ForeignKey('Image.id'))

    user_likes = relationship("User", backref="Comment")

class Image(Base):
    __tablename__ = "Image"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    image = Column(LargeBinary, nullable=False)
    segmented_image = Column(LargeBinary, nullable=True)
    coordintes_classes = Column(JSON, nullable=True)
    upload_date = Column(Date, index=True, nullable=False)

    uploader_id = Column(Integer, ForeignKey('User.id'))
    moderator_id = Column(Integer, ForeignKey('User.id'))

    comment = relationship("Comment", backref="Image")
    user_likes = relationship("User", backref="Image")

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, index=True, nullable=False)

    comment = relationship("Comment", backref="User")
    image = relationship("Image", backref="User")
    comment_likes = relationship("Comment", backref="User")
    comment_user = relationship("Comment", backref="User")
    
    @validates('username')
    def validate_username(self, key, username):
        assert 4 <= len(username) <= 20, "Username length must be between 4 and 20 characters"
        return username

    @validates("email")
    def validate_email(self, key, email):
        assert validate_email_format(email), "Invalid email address"
        return email

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)