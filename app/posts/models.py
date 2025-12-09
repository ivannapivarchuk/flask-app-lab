from datetime import datetime
import enum
from sqlalchemy import Integer, String, Text, DateTime, Enum as SAEnum, ForeignKey, Boolean, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db
from app.users.models import User

class PostCategory(enum.Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag '{self.name}'>"


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(SAEnum(PostCategory), default=PostCategory.other, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"