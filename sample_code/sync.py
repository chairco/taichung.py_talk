#-*- coding: utf-8
import socket
import time


URLS = ['/foo', '/bar']


def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            return


if __name__ == '__main__':
    start = time.time()
    for url in URLS:
        get(url)

    print(f"Sync took {time.time() - start:.1f} sec")
