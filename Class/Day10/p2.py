import threading
import time

def thread_info():
    current_thread = threading.current_thread()
    print(f"Thread Name:{current_thread.name}")
    print(f"Thread ID:{current_thread.native_id}")
    print(f"Is Daemon:{current_thread.daemon}")

print("Main thread:")
thread_info()