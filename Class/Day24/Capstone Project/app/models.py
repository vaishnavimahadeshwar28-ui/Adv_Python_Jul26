# app/models.py

"""

SQLAlchemy ORM models.

"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text

from sqlalchemy.sql import func

from app.database import Base


class Product(Base):

    """Product model representing inventory items."""

    

    __tablename__ = "products"

    

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False, index=True)

    description = Column(Text, nullable=True)

    price = Column(Float, nullable=False)

    stock = Column(Integer, nullable=False, default=0)

    category = Column(String(100), nullable=True)

    sku = Column(String(50), unique=True, index=True, nullable=False)

    is_active = Column(Boolean, default=True)

    external_id = Column(String(100), nullable=True)  # For external enrichment

    external_data = Column(Text, nullable=True)  # JSON string from external API

    created_at = Column(DateTime, server_default=func.now())

    updated_at = Column(DateTime, onupdate=func.now())

    

    def __repr__(self):

        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock})>"
