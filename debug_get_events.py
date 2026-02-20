import asyncio
import inspect
from eventyay.async_client import AsyncEventyayClient
from eventyay.models import EventList

async def debug():
    client = AsyncEventyayClient()
    print(f"--- Client Debug ---")
    print(f"Method Address: {hex(id(client.get_events))}")
    print(f"Method Object: {client.get_events}")
    print(f"Method Source File: {inspect.getfile(client.get_events)}")
    
    # Mock _get at the instance level
    async def mock_get(endpoint, params=None):
        print(f"INTERCEPTED: _get('{endpoint}') called")
        return {"data": [], "links": {}, "meta": {}}
    
    client._get = mock_get
    
    print("Calling client.get_events()...")
    result = await client.get_events()
    print(f"Result Type: {type(result)}")
    print(f"Result Value: {result}")

if __name__ == "__main__":
    asyncio.run(debug())
