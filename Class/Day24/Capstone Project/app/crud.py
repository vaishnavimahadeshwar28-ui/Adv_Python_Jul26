# app/crud.py

"""

CRUD operations for products.

"""

from sqlalchemy.orm import Session

from sqlalchemy import or_, and_, func

from typing import Optional, List, Dict, Any

import logging

from app.models import Product

from app.schemas import ProductCreate, ProductUpdate

from app.decorators import log_execution

logger = logging.getLogger(__name__)


@log_execution

def get_product(db: Session, product_id: int) -> Optional[Product]:

    """Get a product by ID."""

    return db.query(Product).filter(Product.id == product_id).first()


@log_execution

def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:

    """Get a product by SKU."""

    return db.query(Product).filter(Product.sku == sku.upper()).first()


@log_execution

def get_products(

    db: Session,

    skip: int = 0,

    limit: int = 100,

    search: Optional[str] = None,

    category: Optional[str] = None,

    min_price: Optional[float] = None,

    max_price: Optional[float] = None,

    in_stock: Optional[bool] = None,

    is_active: Optional[bool] = True

) -> tuple[List[Product], int]:

    """

    Get products with filtering and pagination.

    Returns (products, total_count).

    """

    query = db.query(Product)

    

    # Apply filters

    if is_active is not None:

        query = query.filter(Product.is_active == is_active)

    

    if search:

        query = query.filter(

            or_(

                Product.name.ilike(f"%{search}%"),

                Product.sku.ilike(f"%{search}%"),

                Product.description.ilike(f"%{search}%")

            )

        )

    

    if category:

        query = query.filter(Product.category == category)

    

    if min_price is not None:

        query = query.filter(Product.price >= min_price)

    

    if max_price is not None:

        query = query.filter(Product.price <= max_price)

    

    if in_stock is not None:

        if in_stock:

            query = query.filter(Product.stock > 0)

        else:

            query = query.filter(Product.stock == 0)

    

    # Get total count

    total = query.count()

    

    # Apply pagination and ordering

    products = query.order_by(Product.id).offset(skip).limit(limit).all()

    

    return products, total


@log_execution

def create_product(db: Session, product_data: ProductCreate) -> Product:

    """Create a new product."""

    # Check for duplicate SKU

    existing = get_product_by_sku(db, product_data.sku)

    if existing:

        raise ValueError(f"Product with SKU {product_data.sku} already exists")

    

    db_product = Product(**product_data.model_dump())

    db.add(db_product)

    db.commit()

    db.refresh(db_product)

    

    logger.info(f"Created product: {db_product.id} - {db_product.name}")

    return db_product


@log_execution

def update_product(

    db: Session,

    product_id: int,

    product_data: ProductUpdate

) -> Optional[Product]:

    """Update a product."""

    db_product = get_product(db, product_id)

    if not db_product:

        return None

    

    # Check SKU uniqueness if updating SKU

    if product_data.sku is not None:

        existing = get_product_by_sku(db, product_data.sku)

        if existing and existing.id != product_id:

            raise ValueError(f"Product with SKU {product_data.sku} already exists")

    

    # Update fields

    update_data = product_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():

        setattr(db_product, field, value)

    

    db.commit()

    db.refresh(db_product)

    

    logger.info(f"Updated product: {db_product.id} - {db_product.name}")

    return db_product


@log_execution

def delete_product(db: Session, product_id: int) -> bool:

    """Delete a product (hard delete)."""

    db_product = get_product(db, product_id)

    if not db_product:

        return False

    

    db.delete(db_product)

    db.commit()

    

    logger.info(f"Deleted product: {product_id}")

    return True


@log_execution

def update_product_stock(db: Session, product_id: int, quantity: int) -> Optional[Product]:

    """Update product stock (add or subtract)."""

    db_product = get_product(db, product_id)

    if not db_product:

        return None

    

    new_stock = db_product.stock + quantity

    if new_stock < 0:

        raise ValueError(f"Not enough stock. Current: {db_product.stock}, Requested: {-quantity}")

    

    db_product.stock = new_stock

    db.commit()

    db.refresh(db_product)

    

    logger.info(f"Updated stock for product {product_id}: {new_stock}")

    return db_product


@log_execution

def get_categories(db: Session) -> List[str]:

    """Get all unique categories."""

    results = db.query(Product.category).distinct().filter(

        Product.category.isnot(None)

    ).all()

    return [r[0] for r in results if r[0]]


@log_execution

def get_inventory_stats(db: Session) -> Dict[str, Any]:

    """Get inventory statistics."""

    total_products = db.query(Product).count()

    active_products = db.query(Product).filter(Product.is_active == True).count()

    total_stock = db.query(func.sum(Product.stock)).scalar() or 0

    low_stock = db.query(Product).filter(

        Product.is_active == True,

        Product.stock > 0,

        Product.stock <= 10

    ).count()

    out_of_stock = db.query(Product).filter(

        Product.is_active == True,

        Product.stock == 0

    ).count()

    

    return {

        "total_products": total_products,

        "active_products": active_products,

        "total_stock": total_stock,

        "low_stock": low_stock,

        "out_of_stock": out_of_stock

    }
