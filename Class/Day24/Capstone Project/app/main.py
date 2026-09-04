# app/main.py

"""

Main FastAPI application.

"""

from fastapi import FastAPI, HTTPException, status

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import logging

from contextlib import asynccontextmanager

from app.database import engine, Base

from app.routers import products, inventory

from app.external import ExternalAPIClient, external_client

from app.decorators import cache

# Configure logging

logging.basicConfig(

    level=logging.INFO,

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

)

logger = logging.getLogger(__name__)


@asynccontextmanager

async def lifespan(app: FastAPI):

    """

    Lifespan context manager for startup and shutdown events.

    """

    # Startup

    logger.info("Starting Inventory Management Platform...")

    

    # Create database tables

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables created")

    

    # Initialize external client

    import os

    from dotenv import load_dotenv

    load_dotenv()

    

    global external_client

    external_client = ExternalAPIClient(

        base_url=os.getenv("EXTERNAL_API_URL", "https://api.example.com"),

        api_key=os.getenv("EXTERNAL_API_KEY", "test-key")

    )

    logger.info("External API client initialized")

    

    yield

    

    # Shutdown

    logger.info("Shutting down Inventory Management Platform...")

    if external_client:

        await external_client.close()

    cache.clear()

    logger.info("Cleanup complete")


# Create FastAPI application

app = FastAPI(

    title="Inventory Management Platform",

    description="Complete inventory management system with external data enrichment",

    version="1.0.0",

    lifespan=lifespan

)

# Configure CORS

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# Include routers

app.include_router(products.router)

app.include_router(inventory.router)


# ===== Health Check =====

@app.get("/health")

async def health_check():

    """Health check endpoint."""

    return {

        "status": "healthy",

        "service": "inventory-platform",

        "version": "1.0.0"

    }


# ===== Global Exception Handlers =====

@app.exception_handler(HTTPException)

async def http_exception_handler(request, exc):

    """Handle HTTP exceptions."""

    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "error": True,

            "status_code": exc.status_code,

            "detail": exc.detail

        }

    )


@app.exception_handler(Exception)

async def general_exception_handler(request, exc):

    """Handle all other exceptions."""

    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")

    return JSONResponse(

        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

        content={

            "error": True,

            "status_code": 500,

            "detail": "An internal error occurred"

        }

    )


# ===== Root Endpoint =====

@app.get("/")

async def root():

    """Root endpoint with API information."""

    return {

        "service": "Inventory Management Platform",

        "version": "1.0.0",

        "endpoints": {

            "products": "/products",

            "inventory": "/inventory",

            "docs": "/docs",

            "health": "/health"

        }

    }
