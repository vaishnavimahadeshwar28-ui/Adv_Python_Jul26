# Global Interpreter Lock (GIL)
# GIL is a mutex, prevents multiple native threads from executing python bytecode
# GIL like a single key to a room, only one person can be inside the room at any given point of time
import time
from threading import Thread

def cpu_bound_task():
    result = 0
    for i in range(10_000_000):
        result+=i
    return result

def io_bound_task():
    time.sleep(4)
    return "Done"

if __name__ == "__main__":
    print("Starting CPU based task")
    cpu_result = cpu_bound_task
    print("Cpu bound result:",cpu_result)

    print("Starting IO based task")
    io_result = io_bound_task()
    print("IO-bound result",io_result)

