import os

directory = "/home/lightning/eventyay-python-sdk/eventyay"
for f in os.listdir(directory):
    if f.endswith('.py'):
        path = os.path.join(directory, f)
        with open(path, 'r') as file:
            content = file.read()
            
        new_content = content.replace('response = self._get(', 'response_data = self._get(')
        new_content = new_content.replace('response = self._post(', 'response_data = self._post(')
        new_content = new_content.replace('response = self._patch(', 'response_data = self._patch(')
        new_content = new_content.replace('response = self._delete(', 'response_data = self._delete(')
        new_content = new_content.replace('response = await self._get(', 'response_data = await self._get(')
        new_content = new_content.replace('response = await self._post(', 'response_data = await self._post(')
        new_content = new_content.replace('response = await self._patch(', 'response_data = await self._patch(')
        new_content = new_content.replace('response = await self._delete(', 'response_data = await self._delete(')
        
        # specific fix for async_mixins.py import
        if "async_mixins.py" in f:
            new_content = new_content.replace(
                "from .models import (\nfrom .utils import parse_jsonapi_resource, parse_jsonapi_list, build_jsonapi_payload\n    Organizer",
                "from .utils import parse_jsonapi_resource, parse_jsonapi_list, build_jsonapi_payload\nfrom .models import (\n    Organizer"
            )

        if "users.py" in f or "async_mixins.py" in f:
            new_content = new_content.replace(
                'app_json = {"data": {"type": "user", "id": str(user_id), "attributes": payload}}\n        response_data = self._patch(f"users/{user_id}", json=app_json)',
                'payload_wrap = build_jsonapi_payload("user", payload, resource_id=str(user_id))\n        response_data = self._patch(f"users/{user_id}", json=payload_wrap)'
            )
            new_content = new_content.replace(
                'app_json = {"data": {"type": "user", "id": str(user_id), "attributes": payload}}\n        response_data = await self._patch(f"users/{user_id}", json=app_json)',
                'payload_wrap = build_jsonapi_payload("user", payload, resource_id=str(user_id))\n        response_data = await self._patch(f"users/{user_id}", json=payload_wrap)'
            )

        if new_content != content:
            with open(path, 'w') as file:
                file.write(new_content)
            print(f'Fixed {f}')
