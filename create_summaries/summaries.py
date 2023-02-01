import json
import asyncio

import aiohttp
from decouple import config


POST_URL = config("POST_URL")


async def create_summaries(title, summary, url, session):
    payload = {'title': title, 'summary': summary, 'url': url}
    async with session.post(f"{POST_URL}", data=payload) as response:
        result = await response.text()
        return result


async def main(event):
    response_payload = event['responsePayload']
    details = json.loads(response_payload)
    async with aiohttp.ClientSession() as session:
        tasks = [create_summaries(title=detail['title'], summary=detail['summary'], url=detail['url'], session=session)
                 for detail in details]
        list_of_tasks = await asyncio.gather(*tasks)
        return list_of_tasks


def lambda_handler(event, context):
    asyncio.run(main(event=event))
