# app/routers/inventory.py

"""

Inventory management endpoints.

"""

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from typing import List, Dict, Any

import logging

from app.database import get_db

from app.schemas import (

    ProductResponse,

    ProductEnrichmentResponse,

    BatchEnrichmentResponse

)

from app.crud import (

    get_product,

    update_product_stock,

    get_inventory_stats

)

from app.dependencies import get_product_by_id

from app.external import get_external_client, ExternalAPIClient

from app.decorators import log_execution, monitor_performance

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/stats")

@log_execution

@monitor_performance(threshold=0.5)

def get_inventory_stats_endpoint(

    db: Session = Depends(get_db)

):

    """

    Get inventory statistics.

    """

    return get_inventory_stats(db)


@router.patch("/stock/{product_id}")

@log_execution

def update_stock_endpoint(

    product_id: int,

    quantity: int,

    db: Session = Depends(get_db),

    existing_product: ProductResponse = Depends(get_product_by_id)

):

    """

    Update product stock (positive to add, negative to subtract).

    """

    try:

        product = update_product_stock(db, product_id, quantity)

        return {

            "id": product.id,

            "name": product.name,

            "stock": product.stock,

            "message": f"Stock updated by {quantity} units"

        }

    except ValueError as e:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail=str(e)

        )


@router.get("/enrich/{product_id}", response_model=ProductEnrichmentResponse)

@log_execution

@monitor_performance(threshold=1.0)

async def enrich_product_endpoint(

    product_id: int,

    db: Session = Depends(get_db),

    product: ProductResponse = Depends(get_product_by_id),

    external: ExternalAPIClient = Depends(get_external_client)

):

    """

    Enrich a single product with external data.

    """

    # Fetch external data

    try:

        external_data = await external.get_product_data(product.sku)

    except Exception as e:

        raise HTTPException(

            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,

            detail=f"External API error: {str(e)}"

        )

    

    if not external_data:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"No external data found for SKU {product.sku}"

        )

    

    # Update product with external data

    db_product = get_product(db, product_id)

    db_product.external_id = external_data.get('id')

    db_product.external_data = external_data

    

    db.commit()

    db.refresh(db_product)

    

    return ProductEnrichmentResponse(

        id=db_product.id,

        name=db_product.name,

        enriched_data=external_data,

        enriched_at=db_product.updated_at

    )


@router.post("/enrich/batch", response_model=BatchEnrichmentResponse)

@log_execution

@monitor_performance(threshold=2.0)

async def enrich_batch_endpoint(

    product_ids: List[int],

    db: Session = Depends(get_db),

    external: ExternalAPIClient = Depends(get_external_client)

):

    """

    Enrich multiple products with external data.

    """

    if not product_ids:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Product IDs list cannot be empty"

        )

    

    # Get products

    products = []

    sku_to_id = {}

    for pid in product_ids:

        product = get_product(db, pid)

        if product:

            products.append(product)

            sku_to_id[product.sku] = product.id

    

    if not products:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="No valid products found"

        )

    

    # Fetch external data

    skus = [p.sku for p in products]

    external_data_map = await external.enrich_multiple_products(skus)

    

    # Update products

    enriched_count = 0

    failed_count = 0

    details = []

    

    for product in products:

        external_data = external_data_map.get(product.sku)

        if external_data:

            product.external_id = external_data.get('id')

            product.external_data = external_data

            enriched_count += 1

            details.append({

                "product_id": product.id,

                "sku": product.sku,

                "status": "enriched"

            })

        else:

            failed_count += 1

            details.append({

                "product_id": product.id,

                "sku": product.sku,

                "status": "failed",

                "reason": "No external data found"

            })

    

    db.commit()

    

    return BatchEnrichmentResponse(

        total=len(products),

        enriched=enriched_count,

        failed=failed_count,

        details=details

    )
