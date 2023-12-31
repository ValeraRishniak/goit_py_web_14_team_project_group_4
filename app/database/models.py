import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, func, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import declarative_base


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
    comment = relationship(
        "ImageComment", secondary=image_m2m_comment, backref="images"
    )


class ImageTag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), unique=True)
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )

    user = relationship("User", backref="tags")


class ImageComment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment_description = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    image_id = Column(
        "image_id", ForeignKey("images.id", ondelete="CASCADE"), default=None
    )
    update_status = Column(Boolean, default=False)

    user = relationship("User", backref="comments")
    image = relationship("Image", backref="comments")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column("role", Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class QR_code(Base):
    __tablename__ = "Qr_codes"

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)

    image_id = Column(Integer, ForeignKey("images.id"))


class BanToken(Base):
    __tablename__ = 'blacklist_tokens'
    
    id = Column(Integer, primary_key=True)
    token = Column(String(500), unique=True, nullable=False)
    banned_on = Column(DateTime, default=func.now())

