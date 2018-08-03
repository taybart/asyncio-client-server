""" A service that keeps track of how many requests per second it is receiving. """
import unittest
import time
import asyncio
import subprocess
from server import Server

loop = asyncio.get_event_loop()

class TestServer(unittest.TestCase):
    def setUp(self):
        self.s = Server(3)
        self.s.setup(loop)

    def test_request_count(self):
        # make sure the server is new
        self.assertEqual(self.s.reqs_s, 0)
        self.assertEqual(self.s.lifetime_requests, 0)
        # run a ping
        loop.create_task(self.s.self_flagellate())
        loop.run_until_complete(self.s.monitor())
        # see if server recieved
        self.assertEqual(self.s.lifetime_requests, 1)
        time.sleep(1)
        # Make sure counter went back down
        self.assertEqual(self.s.reqs_s, 0)
        self.s.teardown()

unittest.main()
