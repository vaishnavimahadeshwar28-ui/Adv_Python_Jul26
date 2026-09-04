# Thread Synchronization: Race condition problem
import threading
import time

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        current = self.value
        time.sleep(0.0001)

        self.value = current + 1

def race_condition_demo():
    counter = Counter()

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

race_condition_demo()