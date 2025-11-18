import asyncio
import os
import crawler
from crawler.url_manager import JsonURLManager

crawler.utils.setup_logging()

source_store_path = './sources'
os.makedirs(source_store_path, exist_ok=True)

crawler_instance = crawler.Crawler(
    'https://buma.wiki',
    source_store_path,
    JsonURLManager(os.path.join(source_store_path, 'data.json'))
)

async def main():
    async with crawler_instance:
        await crawler_instance.download_page('https://buma.wiki/docs/%EA%B9%80%ED%98%84%ED%98%B81')

asyncio.run(main()) # TODO 링크 매니지 json 구현체