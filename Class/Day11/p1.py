import threading
import time

# Simple thread function
def simple_worker(name,delay):
    print(f"Thread {name}: starting")

    time.sleep(delay)

    print(f"Thread {name}: Finished after {delay} seconds")

def create_basic_threads():
    print("Creating threads...")
    # Create thread
    thread1 = threading.Thread(target=simple_worker,args=("A",2))
    thread2 = threading.Thread(target=simple_worker,args=("B",1)) 

    # start threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish before continuing
    thread1.join()
    thread2.join()

    print("All threads finished")

create_basic_threads()

# Thread with multiple arguments
def worker_with_args(name,delay,repeat):
    for i in range(repeat):
        print(f"Thread {name}: Iteration {i+1}")
        time.sleep(delay)

def create_complex_thread():
    thread = threading.Thread(target=worker_with_args,args=("worker", 1, 3))

    thread.start()
    thread.join()

create_complex_thread()