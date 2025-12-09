from app import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
    password: Mapped[str] = mapped_column(String(60), nullable=False)


    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"