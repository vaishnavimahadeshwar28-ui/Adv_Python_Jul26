# Combining FastAPI with SQLAlchemy
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# ===== Database Setup =====
SQLALCHEMY_DATABASE_URL = "sqlite:///./api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ===== Database Models =====
class ProductDB(Base):
    """Product database model."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

Base.metadata.create_all(bind=engine)

# ===== Pydantic Models =====
class ProductCreate(BaseModel):
    """Product creation model."""
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductUpdate(BaseModel):
    """Product update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(BaseModel):
    """Product response model."""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    created_at: datetime

    class Config:
        orm_mode = True


# ===== Database Dependency =====
def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

# ===== CRUD Functions =====
def get_product(db: Session, product_id: int):
    """Get a product by ID."""
    return db.query(ProductDB).filter(ProductDB.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """Get products with pagination."""
    return db.query(ProductDB).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    """Create a new product."""
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    """Update a product."""
    db_product = get_product(db, product_id)

    if not db_product:
        return None

    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    """Delete a product."""
    db_product = get_product(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()

    return True

# ===== API Endpoints =====
@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    """Create a new product."""
    return create_product(db, product)


@app.get("/products", response_model=List[ProductResponse])
async def get_products_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    """Get all products."""
    return get_products(db, skip=skip, limit=limit)


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):

    """Get a product by ID."""
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product

@app.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product."""
    product = update_product(db, product_id, product_update)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product."""
    if not delete_product(db, product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P1:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
