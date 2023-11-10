import enum

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
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


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    image = Column(LargeBinary)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user = relationship("User", backref="images")
    tags = relationship("ImageTag", secondary=image_m2m_tag, backref="images")


class ImageTag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), unique=True)


class ImageComment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment_description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user = relationship("User", backref="comments")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column("role", Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
