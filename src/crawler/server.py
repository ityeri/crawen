import mimetypes
import os.path

import aiofiles
import uvicorn
from fastapi import FastAPI, APIRouter, Response, Request, HTTPException
from fastapi.responses import StreamingResponse
from yarl import URL

from crawler.url_manager import URLManager
from crawler.utils import parsing_utils
from crawler.utils.file import read_in_chunks


class Server:
    def __init__(
            self,
            root_url: URL | str,
            source_store_path: str,
            url_manager: URLManager,
    ):
        self.app = FastAPI()
        self.root_url: URL = URL(root_url)
        self.source_store_path: str = source_store_path
        self.url_manager: URLManager = url_manager

    def setup(self):
        router = APIRouter()
        router.add_api_route('/{path:path}', self.on_route, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        self.app.include_router(router)

    async def on_route(self, path: str, request: Request):
        relative_url = URL(URL(str(request.url)).raw_path_qs)
        url = self.root_url.join(relative_url)
        print('converted:', str(url))
        print('raw:', request.url)

        try:
            file_name = await self.url_manager.get_url(url)
        except KeyError:
            raise HTTPException(status_code=404)

        file_path = os.path.join(self.source_store_path, file_name)
        content_type, _ = mimetypes.guess_type(file_name)

        if parsing_utils.is_text_content_type(content_type):
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                body = await f.read()
                return Response(content=body, media_type=content_type)

        else:
            return StreamingResponse(read_in_chunks(file_path), media_type=content_type)

    def run(self, host: str = '127.0.0.1', port=8000):
        uvicorn.run(self.app, host=host, port=port)