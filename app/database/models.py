import enum

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    func,
    Table,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

image_m2m_comment = Table(
    "image_m2m_comment",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("comment_id", Integer, ForeignKey("comments.id", ondelete="CASCADE")),
)


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    done = Column(Boolean, default=False)
    image_url = Column(String(300))
    transform_url = Column(String(500), nullable=True)
    public_id = Column(String(255))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), default=None)
    
    user = relationship("User", backref="images")
    tags = relationship("ImageTag", secondary=image_m2m_tag, backref="images")
    comment = relationship("ImageComment", secondary=image_m2m_comment, backref="images")



class ImageTag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), unique=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    
    user = relationship('User', backref="tags")


class ImageComment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment_description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey("users.id", ondelete="CASCADE"), default=None)
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), default=None)
    update_status = Column(Boolean, default=False)

    user = relationship('User', backref="comments")
    photo = relationship('Image', backref="comments")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False)
    refresh_token = Column(String(255), nullable=True)
    role = Column("role", Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)


class CropMode(str, enum.Enum):
    fill = "fill"
    thumb = "thumb"
    fit = "fit"
    limit = "limit"
    pad = "pad"
    scale = "scale"


class BGColor(str, enum.Enum):
    black = "black"
    white = "white"
    red = "red"
    green = "green"
    blue = "blue"
    yellow = "yellow"
    gray = "gray"
    brown = "brown"
    transparent = "transparent"


class QR_code(Base):
    __tablename__ = "Qr_codes"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)

    photo_id = Column(Integer, ForeignKey("images.id"))
