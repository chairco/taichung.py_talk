#-*- coding:utf-8 -*-
import socket
import time

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
n_jobs = 0

URLS = ['/foo', '/bar']


def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    callback = lambda: connected_event(s, path)  # closure
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_WRITE, data=callback)


def connected_event(s, path):
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    callback = lambda: readable_event(s, chunks)
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_READ, data=callback)


def readable_event(s, chunks):
    global n_jobs
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable_event(s, chunks)
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ, data=callback)
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        n_jobs -= 1


def eventloop():
    start = time.time()
    for url in URLS:
        get(url)

    while n_jobs:
        events = selector.select()
        for key, mask in events:
            cb = key.data
            cb()
    
    print(f"Event loop took {time.time() - start:.1f} sec")


if __name__ == '__main__':
    eventloop()