# app/schemas.py

"""

Pydantic models for request/response validation.

"""

from pydantic import BaseModel, Field, validator

from typing import Optional, Dict, Any

from datetime import datetime


# ===== Base Schemas =====

class ProductBase(BaseModel):

    """Base product schema."""

    name: str = Field(..., min_length=1, max_length=200)

    description: Optional[str] = None

    price: float = Field(..., gt=0)

    stock: int = Field(0, ge=0)

    category: Optional[str] = Field(None, max_length=100)

    sku: str = Field(..., min_length=1, max_length=50)

    

    @validator('sku')

    def validate_sku(cls, v):

        """Validate SKU format (uppercase, no spaces)."""

        if ' ' in v:

            raise ValueError('SKU must not contain spaces')

        return v.upper()


class ProductCreate(ProductBase):

    """Schema for creating a product."""

    pass


class ProductUpdate(BaseModel):

    """Schema for updating a product (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)

    description: Optional[str] = None

    price: Optional[float] = Field(None, gt=0)

    stock: Optional[int] = Field(None, ge=0)

    category: Optional[str] = Field(None, max_length=100)

    is_active: Optional[bool] = None

    sku: Optional[str] = None

    @validator('sku', always=True)

    def validate_sku_update(cls, v):

        if v is not None:

            if ' ' in v:

                raise ValueError('SKU must not contain spaces')

            return v.upper()

        return v


# ===== Response Schemas =====

class ProductResponse(ProductBase):

    """Schema for product response."""

    id: int

    is_active: bool

    external_id: Optional[str]

    external_data: Optional[Dict[str, Any]]

    created_at: datetime

    updated_at: Optional[datetime]

    

    class Config:

        from_attributes = True

    

    @validator('external_data', pre=True)

    def parse_external_data(cls, v):

        """Parse JSON string to dict if needed."""

        if isinstance(v, str):

            try:

                import json

                return json.loads(v)

            except:

                return None

        return v


class ProductListResponse(BaseModel):

    """Schema for product list response with pagination."""

    items: list[ProductResponse]

    total: int

    page: int

    page_size: int

    pages: int


# ===== Enrichment Schemas =====

class ProductEnrichmentResponse(BaseModel):

    """Schema for enriched product data."""

    id: int

    name: str

    enriched_data: Dict[str, Any]

    enriched_at: datetime


class BatchEnrichmentResponse(BaseModel):

    """Schema for batch enrichment response."""

    total: int

    enriched: int

    failed: int

    details: list[Dict[str, Any]]
