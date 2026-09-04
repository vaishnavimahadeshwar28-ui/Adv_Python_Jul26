# app/dependencies.py

"""

FastAPI dependencies.

"""

from typing import Optional, List

from fastapi import Depends, Query, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db

from app.crud import get_product, get_product_by_sku


def get_product_by_id(

    product_id: int,

    db: Session = Depends(get_db)

):

    """

    Dependency to get a product by ID.

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

):

    """

    Dependency to get a product by SKU.

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

        page: int = Query(1, ge=1, description="Page number"),

        page_size: int = Query(10, ge=1, le=100, description="Items per page")

    ):

        self.page = page

        self.page_size = page_size

        self.skip = (page - 1) * page_size


class ProductFilters:

    """

    Dependency for product filter parameters.

    """

    def __init__(

        self,

        search: Optional[str] = Query(None, description="Search by name, SKU, or description"),

        category: Optional[str] = Query(None, description="Filter by category"),

        min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),

        max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),

        in_stock: Optional[bool] = Query(None, description="Filter by availability"),

        is_active: Optional[bool] = Query(True, description="Filter by active status")

    ):

        self.search = search

        self.category = category

        self.min_price = min_price

        self.max_price = max_price

        self.in_stock = in_stock

        self.is_active = is_active
