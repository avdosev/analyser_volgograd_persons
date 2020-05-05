import asyncio
# from aiomisc import entrypoint
from crawler import download_news
from files import writeJSON
import config as cfg


async def queue_printer(queue):
    while True:
        val = await queue.get()
        writeJSON(cfg.DATA_PATH, val)
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    downloader = asyncio.create_task(download_news(queue))
    printer = asyncio.create_task(queue_printer(queue))
    await asyncio.gather(downloader)
    await queue.join()
    printer.cancel()
    await asyncio.gather(printer, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
