import asyncio
import aiohttp
import time
import pandas as pd
import requests

URL = "http://127.0.0.1:8000/predict"  # replace with your FastAPI endpoint
NUM_REQUESTS = 50
CONCURRENCY = 10
payload = pd.read_csv('inputs.csv').to_dict('records')

# async def fetch(session, i):
#     async with session.post(URL, json=payload) as resp:
#         text = await resp.text()
#         print(f'Done: {i}!')
#         return i, resp.status, text

# async def worker(name, queue, session, results):
#     while True:
#         i = await queue.get()
#         try:
#             res = await fetch(session, i)
#             results.append(res)
#         finally:
#             queue.task_done()

# async def main():
#     queue = asyncio.Queue()
#     for i in range(NUM_REQUESTS):
#         await queue.put(i)

#     results = []
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.create_task(worker(n, queue, session, results)) for n in range(CONCURRENCY)]
#         start = time.time()
#         await queue.join()
#         for t in tasks:
#             t.cancel()
#         end = time.time()

#     print(f"Completed {len(results)} requests in {end-start:.2f}s")


########################
async def fetch(session, i):
    async with session.post(URL, json=payload) as resp:
        data = await resp.json()
        print(f"✅ Request {i} done, {len(data['predictions'])}")
        return data

async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i) for i in range(20)]  # 20 parallel requests
        await asyncio.gather(*tasks)
    print(f"⏱ Total time: {time.time()-start:.2f}s")

def single_request():
    start = time.time()
    r = requests.post(URL, json=payload)
    print(f"⏱ Total time: {time.time()-start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
    single_request()
