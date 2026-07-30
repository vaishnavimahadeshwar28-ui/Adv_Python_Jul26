import asyncio
import time

async def task1():
    print("Starting asychronous work")
    
    print("Task 1.1: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 1.1 done")

    print("Task 1.2: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 1.2 done")

    print("All ASynchronous work done")

async def task2():
    print("Starting asychronous work")
    
    print("Task 2.1: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 2.1 done")

    print("Task 2.2: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 2.2 done")

    print("All ASynchronous work done")

async def task3():
    print("Starting asychronous work")
    
    print("Task 3.1: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 3.1 done")

    print("Task 3.2: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 3.2 done")

    print("All ASynchronous work done")

async def run_concurrently():
    print("Start concurrent execution")

    start = time.time()
    # asyncio.gather: very important function
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    print(f"All tasks completed in {time.time()-start:.2f}s")
    print(f"Results: {results}")

asyncio.run(run_concurrently())