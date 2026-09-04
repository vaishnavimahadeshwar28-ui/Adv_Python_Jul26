# app/external.py

"""

External API client for product data enrichment.

"""

import json

import httpx

from typing import Optional, Dict, Any, List

import asyncio

import logging

from app.decorators import retry, log_execution, cached

logger = logging.getLogger(__name__)


class ExternalAPIClient:

    """Client for external product data API."""

    

    def __init__(self, base_url: str, api_key: str):

        self.base_url = base_url.rstrip('/')

        self.api_key = api_key

        self.timeout = 10.0

        self.client = None

    

    async def _get_client(self) -> httpx.AsyncClient:

        """Get or create HTTP client."""

        if self.client is None:

            self.client = httpx.AsyncClient(

                timeout=self.timeout,

                headers={

                    "Authorization": f"Bearer {self.api_key}",

                    "Content-Type": "application/json"

                }

            )

        return self.client

    

    @retry(max_attempts=3, delay=0.5)

    @log_execution

    @cached(ttl_seconds=300, key_prefix="external")

    async def get_product_data(self, product_id: str) -> Optional[Dict[str, Any]]:

        """

        Fetch product data from external API.

        """

        client = await self._get_client()

        url = f"{self.base_url}/products/{product_id}"

        

        logger.debug(f"Fetching external data for product {product_id}")

        

        try:

            response = await client.get(url)

            response.raise_for_status()

            data = response.json()

            logger.info(f"Successfully fetched data for product {product_id}")

            return data

        except httpx.HTTPStatusError as e:

            logger.error(f"HTTP error fetching product {product_id}: {e.response.status_code}")

            raise

        except Exception as e:

            logger.error(f"Error fetching product {product_id}: {e}")

            raise

    

    @log_execution

    async def enrich_multiple_products(

        self, 

        product_ids: List[str]

    ) -> Dict[str, Optional[Dict[str, Any]]]:

        """

        Fetch data for multiple products concurrently.

        """

        results = {}

        

        # Create tasks for all products

        tasks = {

            product_id: self.get_product_data(product_id)

            for product_id in product_ids

        }

        

        # Execute all tasks concurrently

        for product_id, task in tasks.items():

            try:

                results[product_id] = await task

            except Exception as e:

                logger.error(f"Failed to enrich product {product_id}: {e}")

                results[product_id] = None

        

        return results

    

    async def close(self):

        """Close the HTTP client."""

        if self.client:

            await self.client.aclose()

            self.client = None


# Global client instance (initialized in main)

external_client: Optional[ExternalAPIClient] = None


async def get_external_client() -> ExternalAPIClient:

    """Dependency for external client."""

    if external_client is None:

        raise RuntimeError("External client not initialized")

    return external_client
