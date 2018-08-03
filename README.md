# Asyncio client/server

Write the following in Python3 & asyncio:
- A client that can throttle the number of requests per second it can send concurrently.
- A service that keeps track of how many requests per second it is receiving.

## Deps
`aiohttp 3.3.2`

## Testing
`$ python3 test_server.py`
`$ python3 test_client.py`

## Running
`$ python3 main.py server`
In seperate terminal:
`$ python3 main.py client`

