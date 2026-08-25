# status code & Response Models
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional
app = FastAPI()
class ItemCreate(BaseModel):
    name: str
    price: float
    stock: int

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int

@app.post("/items", response_model=ItemResponse,
        status_code=status.HTTP_201_CREATED )
async def create_item(item: ItemCreate):
    return{
        "id":123,
        "name":item.name,
        "price":item.price,
        "stock":item.stock
    }

@app.delete("/items/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id:int):
    pass

# custom status code
@app.post("/process", status_code=status.HTTP_202_ACCEPTED)
async def process_task(task:dict):
    return{
        "task_id": "task_123",
        "status": "accepted",
        "estimated_completion" : "5 minutes"
    }

# Run our application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P3:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )