import unittest
import time
import asyncio
import subprocess
from server import Server
""" A service that keeps track of how many requests per second it is receiving. """

loop = asyncio.get_event_loop()

class TestServer(unittest.TestCase):
    def setUp(self):
        self.s = Server(3)
        self.s.setup(loop)

    def test_request_count(self):
        self.assertEqual(self.s.reqs_s, 0)
        loop.create_task(self.s.self_flagellate())
        loop.run_until_complete(self.s.monitor())

        #  self.assertEqual(self.s.reqs_s, 1)
        self.assertEqual(self.s.lifetime_requests, 1)
        time.sleep(1)

        print(self.s.reqs_s)
        self.assertEqual(self.s.reqs_s, 0)
        self.s.teardown()

unittest.main()
