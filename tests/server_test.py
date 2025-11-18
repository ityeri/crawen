import asyncio

from crawler import Server
from crawler.url_manager import JsonURLManager

url_manager = JsonURLManager('./sources/data.json')
asyncio.run(url_manager.load())

server = Server(
    'https://buma.wiki',
    './sources',
    url_manager
)
server.setup()

server.run()