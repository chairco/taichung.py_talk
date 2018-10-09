#-*- coding:utf-8 -*-
import alog
import time
import asyncio
import aiohttp


url = 'http://localhost:5000'
URLS = ['/foo', '/bar']


@asyncio.coroutine
def fetch_page(session, url):
    resp = yield from session.get(url)
    if resp.status == 200:
        text = yield from resp.text()
        alog.info(f"GET {resp.url} HTTP/1.0 {resp.status} OK")

    yield from session.close()


async def async_fetch_page(url):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
        if resp.status == 200:
            text = await resp.text()
            alog.info(f"GET {resp.url} HTTP/1.0 {resp.status} OK")


def async_syntax():
    """async syntax
    """
    start = time.time()
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [
        asyncio.ensure_future(async_fetch_page(f"{url}{u}")) for u in URLS
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    alog.info(f'async syntax Coroutines took {time.time() - start:.1f} sec')


def yieldfrom_syntax():
    start = time.time()
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # yield from syntax
    session = aiohttp.ClientSession(loop=loop)
    tasks = [
        #loop.create_task(fetch_page(session, f"{url}/foo")),
        #loop.create_task(fetch_page(session, f"{url}/bar"))
        asyncio.ensure_future(fetch_page(session, f"{url}{u}")) for u in URLS
    ]

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    alog.info(f'yieldfrom syntax Coroutines took {time.time() - start:.1f} sec')


if __name__ == '__main__':
    oldloop = asyncio.get_event_loop()
    async_syntax()
    yieldfrom_syntax()
    asyncio.set_event_loop(oldloop)

