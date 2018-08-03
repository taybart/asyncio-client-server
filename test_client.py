import unittest
import asyncio
from client import Client
""" A client that can throttle the number of requests per second it can send concurrently. """

loop = asyncio.get_event_loop()

class TestClient(unittest.TestCase):
    def setUp(self):
        self.test_rate = 10
        self.test_time = 2
        self.c = Client(self.test_rate, self.test_time)
        self.c.setup(loop)
    def test_rate_limit(self):
        loop.run_until_complete(self.c.makeRequests('http://example.com'))
        self.c.teardown()
        loop.close()
        #  print(self.c.lifetime_requests, self.test_rate * self.test_time)
        self.assertLessEqual(self.c.lifetime_requests, self.test_rate * self.test_time)

unittest.main()
