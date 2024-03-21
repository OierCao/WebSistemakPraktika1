import requests
import time
import random

# Zure ThingSpeak kanalaren Write API Key
CHANNEL_API_KEY = 'RVNPYS0U7ZX42F7J'

# Datuak jeisteko funtzioa
def download_data(channelId):
    metodoa = 'GET'
    url = f'https://api.thingspeak.com/channels/{channelId}/feeds.json'
    headers = { 'Host': 'api.thingspeak',
                'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'api_key': CHANNEL_API_KEY,
        'results': 100
    }

    erantzuna = requests.request(metodoa, url, headers=headers, data=data)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

if __name__ == "__main__":
    download_data('2436265')
