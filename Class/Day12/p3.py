# Solution 1: Mutex Locks
import threading
import time
class SafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            current = self.value
            time.sleep(0.0001)
        
            self.value = current+1
            
    def decrement(self):
        # Manually acquire the lock
        self.lock.acquire()
        try:
            current = self.value
            self.value = current - 1
        finally:
            self.lock.release()

def safe_counter_demo():
    counter = SafeCounter()

    def worker():
        for _ in range(100):
            counter.increment()
    
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Expected: 1000, We got:{counter.value}")
safe_counter_demo()