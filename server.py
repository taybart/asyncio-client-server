"""
Write the following in Python3 & asyncio:
- A service that keeps track of how many requests per second it is receiving.
"""
import time
import asyncio
from aiohttp import web
import aiohttp

"""
Usage:
    loop = asyncio.get_event_loop()
    s = Server()
    s.setup(loop)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        s.teardown()
"""

class Server:
    done = False
    reqs_s = 0
    lifetime_requests = 0

    def __init__(self, killafter=None, verbose=False):
        # Testing/debug
        self.verbose = verbose
        self.killafter = killafter
        self.started = time.monotonic()


    """ Function to keep track of requests per second """
    async def monitor(self):
        while not self.done:
            if not self.done and self.verbose:
                print('                      ', end='\r') # clear old text
                print('Load:', self.reqs_s, 'req/s', end='\r')
            self.reqs_s = 0 # Reset counter after 1s
            await asyncio.sleep(1) # Gather data for 1s
            if self.killafter is not None:
                now = time.monotonic()
                if now - self.started > self.killafter:
                    print('Killafter triggered at: ', now - self.started)
                    self.done = True

    def setup(self, loop):
        print('Setting up server')
        self._loop = loop
        ## Setup aiohttp server
        app = web.Application()
        # Prefer decorators for clairity
        routes = web.RouteTableDef()
        # Simple handler that just returns total lifetime requests
        @routes.get('/')
        async def handle(request):
            self.reqs_s += 1
            self.lifetime_requests += 1
            return web.Response(text='Total lifetime requests: '+str(self.lifetime_requests))
        app.add_routes(routes)
        # Use AppRunner directly so loop.run_forever is not called early
        runner = web.AppRunner(app)
        self._loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner)
        self._loop.run_until_complete(site.start())
        names = sorted(str(s.name) for s in runner.sites)
        print('Server listening on {}'.format(', '.join(names)))
        # Add monitor to loop
        self.runner = runner

    def teardown(self):
        print('Closing server')
        self._loop.create_task(self.runner.cleanup())
        self.done = True
        pending = asyncio.all_tasks(loop=self._loop)
        group = asyncio.gather(*pending)
        self._loop.run_until_complete(group)
        print('Bye.')
    async def self_flagellate(self):
        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()
        async with aiohttp.ClientSession() as session:
            res = await fetch(session, 'http://localhost:8080')
            if self.verbose:
                print(res)
