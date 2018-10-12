#-*- coding:utf-8 -*-
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

import socket
import time


selector = DefaultSelector()
n_jobs = 0

URLS = ['/foo', '/bar']

'''
class Future:
    def __init__(self):
        self.callbacks = []

    def resolve(self):
        for fn in self.callbacks:
            fn()


class Task:
    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            future = next(self.coro)
        except StopIteration:
            return
        future.callbacks.append(self.step)
'''

class Future:

    def __init__(self):
        self.callbacks = None

    def resolve(self):
        self.callbacks()

    def __await__(self):
        yield self


class Task:

    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            f = self.coro.send(None)
        except StopIteration:
            return
        f.callbacks = self.step


async def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, data=f)
    #yield f
    await f

    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        f = Future()
        selector.register(s.fileno(), EVENT_READ, data=f)
        #yield f
        await f
        selector.unregister(s.fileno())
        
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            n_jobs -= 1
            return 


def eventloop():
    start = time.time()

    for url in URLS:
        Task(get(url))
     
    while n_jobs:
        events = selector.select()
        # what next?
        for key, mask in events:
            fut = key.data
            fut.resolve()
    
    print(f'Coroutines took {time.time() - start:.1f} sec')


if __name__ == '__main__':
    eventloop()