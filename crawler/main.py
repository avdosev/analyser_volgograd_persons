import asyncio
from aiomisc import entrypoint
from crawler import download_news


async def queue_printer(queue):
    while True:
        val = await queue.get()
        print(val)
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    downloader = asyncio.create_task(download_news(queue))
    printer = asyncio.create_task(queue_printer(queue))
    await downloader
    await queue.join()
    printer.cancel()
    await asyncio.gather(printer, return_exceptions=True)


if __name__ == '__main__':
    with entrypoint() as loop:
        loop.run_until_complete(main())
