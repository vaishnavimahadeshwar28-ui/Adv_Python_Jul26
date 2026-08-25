# Query Parameter validation
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

#Query Parameter with validation
@app.get("/items")
async def get_items(
    q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z]+$"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of items to skip"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum items to return"
    )
):
    return{"query":q,"skip":skip,"limit":limit}

# Query parameter with Multiple values
@app.get("/filter")
async def filter_items(
    tags:list[str] = Query([], description="Tags to filter by")
):
    return{"tags": tags}

# Run our application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "P2:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
# http://127.0.0.1:8000/items?q=mobile
# http://127.0.0.1:8000/items?q=mobile&skip=10&limit=20
# http://127.0.0.1:8000/filter?tags=python&tags=fastapi