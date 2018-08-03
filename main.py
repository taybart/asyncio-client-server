import sys
import asyncio
from server import Server
from client import Client

loop = asyncio.get_event_loop()
if sys.argv[1] == 'server' or sys.argv[1] == 's':
    s = Server()
    s.setup(loop)
    try:
        loop.run_until_complete(s.monitor())
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        s.teardown()
elif sys.argv[1] == 'client' or sys.argv[1] == 'c':
    c = Client(100)
    c.setup(loop)
    try:
        loop.run_until_complete(c.makeRequests('http://localhost:8080'))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        c.teardown()
        loop.close()
else:
    print('Usage: python3 main.py [server,s,client,c]')
