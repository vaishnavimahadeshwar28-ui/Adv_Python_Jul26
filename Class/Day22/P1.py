# Middleware: Error handling
# Needs to be discussed

from fastapi import FastAPI, HTTPException, status


from fastapi.exceptions import RequestValidationError


from fastapi.responses import JSONResponse


from pydantic import BaseModel


from typing import Optional
from datetime import datetime


app = FastAPI()


# ===== Basic HTTP Exception =====


@app.get("/items/{item_id}")


async def get_item(item_id: int):


    """


    Get an item with proper error handling.


    """


    if item_id < 1:


        raise HTTPException(


            status_code=status.HTTP_400_BAD_REQUEST,


            detail="Item ID must be positive"


        )


   


    if item_id > 100:


        raise HTTPException(


            status_code=status.HTTP_404_NOT_FOUND,


            detail=f"Item {item_id} not found",


            headers={"X-Error": "Item not found"}


        )


   


    return {"item_id": item_id, "name": f"Item {item_id}"}


# ===== Custom Exception Classes =====


class BusinessException(Exception):


    """Custom business logic exception."""


    def __init__(self, message: str, code: str = "BUSINESS_ERROR"):


        self.message = message


        self.code = code


        super().__init__(message)


@app.exception_handler(BusinessException)


async def business_exception_handler(request, exc: BusinessException):


    """Handle custom business exceptions."""


    return JSONResponse(


        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,


        content={


            "error": exc.code,


            "message": exc.message,


            "timestamp": datetime.now().isoformat()


        }


    )


# ===== Using Custom Exception =====


@app.post("/orders")


async def create_order(order_data: dict):


    """


    Create an order with business logic validation.


    """


    if order_data.get("total") < 0:


        raise BusinessException("Order total cannot be negative", "INVALID_TOTAL")

    if order_data.get("items", 0) == 0:
        
        raise BusinessException("Order must have items", "EMPTY_ORDER")

    return {"order_id": 123, "status": "created"}

# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P1:app",  # Replace test with your filename without .py
        host="127.0.0.1",
        port=8000,
        reload=True
    )


