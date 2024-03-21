import json

nireJson='{"id": 2430208, "name": "Nire kanala","description": null,"latitude": "0.0","longitude": "0.0","created_at": "2024-02-12T11:47:44Z","elevation": null,"last_entry_id": null,"public_flag": false,"url": null,"ranking": 30,"metadata": null,"license_id": 0,"github_url": null,"tags": [],"api_keys": [{"api_key": "LGC85OY90UVR1O1P","write_flag": true},{"api_key": "VZ2Z11PNWKFQW4XG","write_flag": false}]}'

jsonLoad=json.loads(nireJson)

id= str(jsonLoad['id'])

apiKey = None
for key in jsonLoad['api_keys']:
    if key['write_flag']:
        apiKey = key['api_key']
        break

with open("pausu11.txt", 'w') as file:
   if apiKey is not None:
       file.write("id: "+ id +" eta Api Key Write:"+ apiKey)
   else:
       file.write('Ez da aurkitu WRITE_API_KEY')
