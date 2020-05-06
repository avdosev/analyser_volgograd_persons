import asyncio
from model import Connection, insertMongo
from crawler import download_news
from files import writeJSON
import sys
sys.path.append("..")
from config import DATA_PATH


async def queue_printer(conn, queue):
    while True:
        val = await queue.get()
        writeJSON(DATA_PATH, val)
        id = insertMongo(conn, "mydatabase", "customers", val)
        queue.task_done()


async def main():
    conn = Connection()

    queue = asyncio.Queue()
    downloader = asyncio.create_task(download_news(queue))
    printer = asyncio.create_task(queue_printer(conn, queue))
    await asyncio.gather(downloader)
    await queue.join()
    printer.cancel()
    await asyncio.gather(printer, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
