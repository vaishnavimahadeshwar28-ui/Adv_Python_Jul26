# Task States
import asyncio
async def demo_task_states():
    # Create a task
    task = asyncio.create_task(asyncio.sleep(2,result="Done"))
    # State: Pending
    print(f"Task pending: {not task.done()}")
    print(f"Task cancellation requested: {task.cancelled()}")

    # Wait for completion
    await task

    #state: done
    print(f"Task pending: {task.done()}")
    print(f"Task result: {task.result()}")

    # Create a cancellable task
    cancellable_task = asyncio.create_task(asyncio.sleep(5))

    await asyncio.sleep(1)
    print("Cancelling task")
    cancellable_task.cancel()

    try:
        await cancellable_task
    except asyncio.CancelledError:
        print("Task was cancelled")

    print(f"Task cancelled: {cancellable_task.cancelled()}")

asyncio.run(demo_task_states()
            