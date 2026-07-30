import time
import asyncio
def sync_work():
    print("Starting Sychronous work")

    print("Task 1: Starting")
    time.sleep(2) # this blocks
    print("Task 1 done")

    print("Task 2: Starting")
    time.sleep(2) # this blocks
    print("Task 2 done")

    print("All Synchronous work done")

async def async_work():
    print("Starting asychronous work")

    print("Task 1: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 1 done")

    print("Task 2: Starting")
    await asyncio.sleep(2) # this not blocks
    print("Task 2 done")

    print("All ASynchronous work done")

start = time.time()
sync_work()
print(f"Synchronous: {time.time() - start:.2f}s")

start1 = time.time()
asyncio.run(async_work())
print(f"ASynchronous: {time.time() - start1:.2f}s")