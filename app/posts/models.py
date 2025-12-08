from datetime import datetime
import enum
from sqlalchemy import Integer, String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app import db


# Створюємо клас для категорій (щоб був вибір зі списку)
class PostCategory(enum.Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


class Post(db.Model):
    __tablename__ = 'posts'

    # Використовуємо новий синтаксис Mapped та mapped_column (SQLAlchemy 2.0)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category: Mapped[PostCategory] = mapped_column(
        SAEnum(PostCategory),
        default=PostCategory.other,
        nullable=False
    )

    from sqlalchemy import Boolean
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    author: Mapped[str] = mapped_column(String(20), default="Anonymous")


    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', category='{self.category.name}')>"