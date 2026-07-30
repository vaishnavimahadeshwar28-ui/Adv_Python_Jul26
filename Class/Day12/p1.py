# Thread identification & Status
import threading
import time
def thread_status_check():
    # Get the currently running threads
    current = threading.current_thread()

    # Get a list of all active threads in the process
    active_threads = threading.enumerate()

    print(f"Current thread: {current.name} (ID: {current.native_id})")
    print(f"Active threads: {len(active_threads)}")

    for thread in active_threads:
        print(f"{thread.name} (Alive: {thread.is_alive()})")

def print_thread_info(thread, indent=0):
    spaces = " " * indent

    print(f"{spaces}Thread: {thread.name}")
    print(f"{spaces}Thread: {thread.native_id}")
    print(f"{spaces}Thread: {thread.daemon}")
    print(f"{spaces}Thread: {thread.is_alive()}")

def demo_thread_info():
    print_thread_info(threading.main_thread())

    print("Creating a working thread")
    def worker():
        print("Inside Worker")
        print_thread_info(threading.current_thread())
        time.sleep(1)

    thread = threading.Thread(target=worker,name="Worker-1")
    thread.start()
    thread.join()

demo_thread_info()