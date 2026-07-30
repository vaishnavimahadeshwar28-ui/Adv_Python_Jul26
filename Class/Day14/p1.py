import asyncio

async def slow_operation():
    print("Slow operation starting")
    await asyncio.sleep(2)
    return "Slow result"

async def demo_await_vs_task():
    # await
    print("Using await")
    result = await slow_operation()
    print(f"Result: {result}")

    # using create_task : runs in background
    print("Create Task")
    task = asyncio.create_task(slow_operation())
    print("Task is runnung in background")

    await asyncio.sleep(1)

    print("This prints here")

    # await 
    result = await task
    print(f"Result: {result}")
asyncio.run(demo_await_vs_task())
