from datetime import datetime
from sqlalchemy import Integer, String, Float, ForeignKey , Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Зв'язок: Одна категорія має багато продуктів
    products: Mapped[List["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category '{self.name}'>"


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # --- НОВЕ ПОЛЕ ---
    # server_default=func.now() змушує базу даних саму ставити час створення.
    # Це автоматично заповнить дату для старих товарів!
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    # -----------------

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __repr__(self):
        return f"<Product '{self.name}'>"