from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue
import time


class Fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.prev > 10000: raise StopIteration
        self.prev, self.curr = self.curr, self.curr + self.prev
        return self.prev


def _data_loader(q, data):
    # data should be iterable
    for _d in data:
        while q.full():
            time.sleep(0.1)
        q.put(_d)


def data_loader(data, max_queue_size=3):
    q = Queue(max_queue_size)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_data_loader, q, data)
        while future.running() or not q.empty():
            if q.empty():
                time.sleep(0.1)
                continue
            yield q.get()


if __name__ == "__main__":
    for batch in data_loader(Fib()):
        print(batch)
        # train your model here
