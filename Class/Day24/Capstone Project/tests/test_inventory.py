# app/dependencies.py
"""
Dependency injection for FastAPI endpoints.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import get_product, get_product_by_sku
from app.schemas import ProductResponse


def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
) -> ProductResponse:
    """
    Dependency that retrieves a product by ID.
    Raises 404 if not found.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


def get_product_by_sku_or_404(
    sku: str,
    db: Session = Depends(get_db)
) -> ProductResponse:
    """
    Dependency that retrieves a product by SKU.
    Raises 404 if not found.
    """
    product = get_product_by_sku(db, sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU {sku} not found"
        )
    return product


class PaginationParams:
    """
    Dependency for pagination parameters.
    """
    def __init__(
        self,
        page: int = 1,
        page_size: int = 20
    ):
        self.page = max(1, page)
        self.page_size = min(100, max(1, page_size))
        self.skip = (self.page - 1) * self.page_size


class ProductFilters:
    """
    Dependency for product filters.
    """
    def __init__(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        is_active: Optional[bool] = None
    ):
        self.search = search
        self.category = category
        self.min_price = min_price
        self.max_price = max_price
        self.in_stock = in_stock
        self.is_active = is_active