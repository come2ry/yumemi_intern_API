import asyncio
import aiohttp
from fastapi.logger import logger as fastapi_logger
import re
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl
import io
import os
from google.cloud import vision
from google.oauth2 import service_account
if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd()+"../")
from app.core.config import settings


image_url_pattern = re.compile(
    r"(https?:\/\/[^:]*\.(?:png|PNG|jpg|JPG|jpeg|JPEG|gif|GIF|svg|SVG))")

# textから画像のurlを正規表現で取得
def extract_image_url_from_text(text: str) -> List[AnyHttpUrl]:
    urls = image_url_pattern.findall(text)
    return list(set(urls))

# 画像のurlのリストを非同期的にVision APIにかけてOCRし、画像内の文字列を取得
async def extract_text_from_image_by_urls_with_OCR(urls: List[AnyHttpUrl]) -> str:
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(vision_api_fetch_all(urls))
    texts = []
    for response in responses:
        text = []
        res = response.get('responses', None)
        if not res is None:
            fulltexts = [r.get('fullTextAnnotation', None) for r in res]
            text = [fulltext.get('text', None) for fulltext in fulltexts if not fulltext is None]
            texts += [t.replace("\n", "") for t in text if not t is None]

    return await " ".join(texts)


# Google Vision API Fetch
async def vision_api_fetch(session, url):
    """Execute an http call async
    Args:
      session: contexte for making the http call
      url: URL to call
    Return:
      responses: A dict like object containing http response
    """

    async with session.post(
        settings.VISION_API_LOCATION,
        json={
            "requests": [
            {
            "image": {
                "source": {
                    "imageUri": url
                }
            },
            "features": [
                {
                    "type": "TEXT_DETECTION"
                }
            ],
            "imageContext": {
                "languageHints": ["ja-JP"]
            }
            }
            ]
        }
    ) as response:
        resp = await response.json()
        return resp

# Google Vision API Fetch All
async def vision_api_fetch_all(urls):
    """ Gather many HTTP call made async
    Args:
      urls: a list of string
    Return:
      responses: A list of dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                vision_api_fetch(
                    session,
                    url,
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

if __name__ == '__main__':
    text = "testtest.png"
    urls = extract_image_url_from_text(text)
    print(urls)
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(vision_api_fetch_all(urls))
    texts = []
    print(len(responses))
    for response in responses:
        text = []
        res = response.get('responses', None)
        if not res is None:
            fulltexts = [r.get('fullTextAnnotation', None) for r in res]
            text = [fulltext.get('text', None) for fulltext in fulltexts if not fulltext is None]
            texts += [t.replace("\n", "") for t in text if not t is None]

    print(texts)
