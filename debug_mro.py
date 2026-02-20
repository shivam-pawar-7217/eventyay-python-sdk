import asyncio
import inspect
from eventyay.async_client import AsyncEventyayClient
from eventyay.models import EventList

async def debug():
    client = AsyncEventyayClient()
    print(f"MRO: {AsyncEventyayClient.__mro__}")
    
    method = getattr(client, 'get_events', None)
    if method:
        print(f"get_events source: {inspect.getsource(method)}")
        print(f"get_events file: {inspect.getfile(method)}")
    else:
        print("get_events not found!")

if __name__ == "__main__":
    asyncio.run(debug())
