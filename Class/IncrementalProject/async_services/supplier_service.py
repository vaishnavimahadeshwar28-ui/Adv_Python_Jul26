import asyncio
import random

async def check_supplier(product_name,supplier_name):
    print(f"Connecting to {supplier_name}...")

    # Simulation of network
    await asyncio.sleep(random.randint(1,3))

    stock_status = random.choice(["In Stock", "Limited Stock", "Out of Stock"])

    return {
        "product": product_name,
        "supplier": supplier_name,
        "status": stock_status
    }

async def supplier_lookup(products):
    suppliers = {
        "Laptop": "Lenovo",
        "Wireless Mouse":"Logitech",
        "Mechanical Keyboard":"Redragon"
    }

    tasks = []

    for product in products:
        supplier = suppliers.get(product.name,"Unknown")

        tasks.append(
            check_supplier(product.name,supplier)
        )
    return await asyncio.gather(*tasks)