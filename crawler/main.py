import asyncio
from dbmodel import Connection, Mongo
from crawler import download_news
from files import writeJSON
import sys
sys.path.append("..")
from config import DATA_PATH
from dbconfig import TABLE_NAME, DATABASE_NAME


async def queue_printer(mongo, queue):
    while True:
        val = await queue.get()
        writeJSON(DATA_PATH, val)
        id = mongo.insert(TABLE_NAME, val)
        queue.task_done()


async def main():
    conn = Connection().getConnection()
    mongo = Mongo(conn, DATABASE_NAME)

    queue = asyncio.Queue()
    downloader = asyncio.create_task(download_news(queue))
    printer = asyncio.create_task(queue_printer(mongo, queue))
    await asyncio.gather(downloader)
    await queue.join()
    printer.cancel()
    await asyncio.gather(printer, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
