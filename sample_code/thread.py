#-*- coding: utf-8 -*-
import concurrent.futures
import time

from sync import get


URLS = ['/foo', '/bar']


start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_to_url = {executor.submit(get, url): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))


print(f'Multithreading took {time.time() - start:.1f} sec')
