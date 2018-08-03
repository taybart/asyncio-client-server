"""
Write the following in Python3 & asyncio:
- A client that can throttle the number of requests per second it can send concurrently.
"""

import time
import asyncio
import aiohttp

"""
Usage:
    loop = asyncio.get_event_loop()
    c = Client(rate=100)
    c.setup(loop)
    try:
        loop.run_until_complete(c.makeRequests('http://localhost:8080'))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        c.teardown()
        loop.close()
"""

class Client:
    done = False
    lifetime_requests = 0

    def __init__(self, rate, killafter=None, verbose=False):
        self.tokens = rate
        self.rate = rate
        # Use monotonic time for async
        self.updated_at = time.monotonic()
        # Testing/debug
        self.verbose = verbose
        self.killafter = killafter
        self.started = time.monotonic()

    async def get(self, *args, **kwargs):
        await self.wait_for_token()
        return self.client.get(*args, **kwargs)

    async def wait_for_token(self):
        while self.tokens < 1:
            self.add_new_tokens()
            await asyncio.sleep(0.01)
        # Use up a slot
        self.tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self.updated_at
        # Update based on RATE, potentially not the best
        new_tokens = time_since_update * self.rate
        if new_tokens > 1:
            self.tokens = min(self.tokens + new_tokens, self.rate)
            self.updated_at = now


    async def makeRequests(self, url):
        print('Requesting', url)
        while not self.done:
            async with await self.get(url) as resp:
                if self.verbose:
                    print(await resp.text())
                self.lifetime_requests += 1

    def setup(self, loop):
        print('Setting up client')
        self._loop = loop
        self.client = aiohttp.ClientSession(loop=loop)
        loop.create_task(self.monitor())


    async def monitor(self):
        if self.killafter is not None:
            while not self.done:
                await asyncio.sleep(0.5)
                now = time.monotonic()
                if now - self.started > self.killafter:
                    print('Killafter triggered at: ', now - self.started)
                    self.done = True

    def teardown(self):
        print('Stopping requests')
        # Let requests finish
        self.done = True
        pending = asyncio.all_tasks(loop=self._loop)
        group = asyncio.gather(*pending)
        self._loop.run_until_complete(group)
        self._loop.run_until_complete(self.client.close())
        print('Bye.')

loop = asyncio.get_event_loop()
c = Client(100, 2)
c.setup(loop)
try:
      loop.run_until_complete(c.makeRequests('http://localhost:8080'))
except KeyboardInterrupt:
      print('KeyboardInterrupt')
finally:
      c.teardown()
      loop.close()
