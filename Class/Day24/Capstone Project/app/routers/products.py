# app/routers/products.py
"""
Product management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.crud import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
    get_categories,
    get_product_by_sku
)
from app.dependencies import (
    get_product_by_id,
    get_product_by_sku_or_404,  # ADDED: Import the missing dependency
    PaginationParams,
    ProductFilters
)
from app.decorators import log_execution, cached

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductListResponse)
@log_execution
@cached(ttl_seconds=60, key_prefix="products_list")
def get_products_endpoint(
    pagination: PaginationParams = Depends(),
    filters: ProductFilters = Depends(),
    db: Session = Depends(get_db)
):
    """
    Get all products with filtering and pagination.
    """
    products, total = get_products(
        db,
        skip=pagination.skip,
        limit=pagination.page_size,
        search=filters.search,
        category=filters.category,
        min_price=filters.min_price,
        max_price=filters.max_price,
        in_stock=filters.in_stock,
        is_active=filters.is_active
    )
    
    return ProductListResponse(
        items=products,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/categories", response_model=List[str])
@log_execution
@cached(ttl_seconds=300, key_prefix="categories")
def get_categories_endpoint(
    db: Session = Depends(get_db)
):
    """Get all unique categories."""
    return get_categories(db)


@router.get("/{product_id}", response_model=ProductResponse)
@log_execution
@cached(ttl_seconds=60, key_prefix="product_detail")
def get_product_endpoint(
    product: ProductResponse = Depends(get_product_by_id)
):
    """
    Get a product by ID.
    """
    return product


@router.get("/sku/{sku}", response_model=ProductResponse)
@log_execution
@cached(ttl_seconds=60, key_prefix="product_sku")
def get_product_by_sku_endpoint(
    product: ProductResponse = Depends(get_product_by_sku_or_404)  # Now defined
):
    """
    Get a product by SKU.
    """
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
@log_execution
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product.
    """
    try:
        return create_product(db, product_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{product_id}", response_model=ProductResponse)
@log_execution
def update_product_endpoint(
    product_data: ProductUpdate,
    product_id: int,
    db: Session = Depends(get_db),
    existing_product: ProductResponse = Depends(get_product_by_id)
):
    """
    Update a product.
    """
    try:
        product = update_product(db, product_id, product_data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_execution
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    existing_product: ProductResponse = Depends(get_product_by_id)
):
    """
    Delete a product.
    """
    if not delete_product(db, product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )