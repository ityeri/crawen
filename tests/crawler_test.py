import asyncio
import os
import crawler
from crawler.url_manager import JsonURLManager

crawler.utils.setup_logging()

source_store_path = './sources'
os.makedirs(source_store_path, exist_ok=True)
url_manager = JsonURLManager(os.path.join(source_store_path, 'data.json'))
asyncio.run(url_manager.load())

crawler_instance = crawler.Crawler(
    'https://namu.wiki',
    source_store_path,
    url_manager
)

async def main():
    async with crawler_instance:
        await crawler_instance.download_page('https://namu.wiki')

asyncio.run(main()) # TODO 링크 매니지 json 구현체