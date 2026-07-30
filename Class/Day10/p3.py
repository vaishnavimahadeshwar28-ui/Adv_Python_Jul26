# Thread Life Cycle
import threading
import time  

class ThreadLifecycle:
    
    @staticmethod
    def worker_thread(name):
       # Thread has started running
        print(f"Thread {name}: Running")

        # Simulate a blocked state (sleep represents waiting)
        print(f"Thread {name}: Sleeping")
        time.sleep(2)

        # Thread finishes its work
        print(f"Thread {name}: Done")

    @staticmethod
    def demonstrate():
       # NEW: create the thread object
        print("1. NEW: Creating thread object")
        thread = threading.Thread(
            target=ThreadLifecycle.worker_thread,
            args=("Worker-1",)
        )

        # READY: start() makes the thread ready/runnable
        print("2. READY: Starting thread")
        thread.start()

        # RUNNING: the thread is now executing worker_thread
        print("3. RUNNING: Thread is executing")

        # BLOCKED: the worker thread will be sleeping for a while
        print("4. BLOCKED: Thread may be sleeping or waiting")
        time.sleep(1)  # Main thread sleeps briefly

        # Check liveness while worker may still be running
        print("5. Check if thread is alive")
        print(f"Thread is alive: {thread.is_alive()}")

        # TERMINATED: join waits for thread to finish
        print("6. TERMINATED: Wait for thread to finish")
        thread.join()
        print(f"Thread is alive: {thread.is_alive()}")

ThreadLifecycle.demonstrate()