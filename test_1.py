import json
import aiohttp
import asyncio

import requests

LLAMA_URL = 'http://127.0.0.1:8080/stream'
SPEECH_SERVER_URL = "http://localhost:8006/say"
WAIT_ADDRESS_TIMEOUT = 0.1


def say(phrase):
    # time.sleep(WAIT_ADDRESS_TIMEOUT)
    try:
        requests.post(SPEECH_SERVER_URL, json={"phrase": phrase},timeout=1e-10)
    except requests.exceptions.ReadTimeout: 
        pass


async def get_json_events():
    async with aiohttp.ClientSession() as session:
        async with session.get(LLAMA_URL) as resp:
            while True:
                chunk = await resp.content.readline()
                # await asyncio.sleep(1)  # artificially long delay

                if not chunk:
                    break
                yield json.loads(chunk.decode("utf-8"))


async def main():
    async for event in get_json_events():
        say(event["data"])
        print(event)


asyncio.run(main())



# def get_json_events_sync():
#     with requests.get(url, stream=True) as r:
#         for line in r.iter_lines():
#             yield json.loads(line.decode("utf-8"))


# for it, event in enumerate(get_json_events_sync()):
#     print(it, event)