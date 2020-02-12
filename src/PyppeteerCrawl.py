# https://medium.com/z1digitalstudio/pyppeteer-the-snake-charmer-f3d1843ddb19

import typing
try:
    from pyppeteer import launch
except ImportError:
    from typing_extensions import Coroutine
    typing.Coroutine = Coroutine
    from pyppeteer.launcher import launch  # work as the next
    # from pyppeteer import launch
    from typing import Any, Callable, Coroutine, Dict, List, Optional

import pprint
import asyncio
# from pyppeteer import launch
import collections

Link = collections.namedtuple("Link", ["href", "text"])

async def get_browser():
    return await launch(headless=True, ignoreHTTPSErrors=True, args=['--no-sandbox'])
    # return await launch({"headless": False})


async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return await page.content()


# async def extract_data(page):
#     result = []
#     # Select tr with a th and td descendant from table
#     elements = await page.xpath(
#         '//a[contains(@href,"/")]')
#     # Extract data
#     for element in elements:
#         row = await page.evaluate(
#             '''(element) => {
#                     href = element.getAttribute("href");
#                     text = element.textContent;
#                     return [href, text]
#                 }
#             ''',
#             element)
#         result.append(Link(href=row[0], text=row[1]))
#     return result


# async def extract(browser, url):
#     return await get_page(browser, url)



async def extract_all(url):
    browser = await get_browser()
    # for name, url in languages.items():
    return await get_page(browser, url)

def run_crawl(url):
    loop = asyncio.get_event_loop()
    # try:
    result = loop.run_until_complete(extract_all(url))
    # finally:
    #     loop.close()

    return result


# if __name__ == "__main__":

#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(extract_all(languages))

#     pprint.pprint(result)
