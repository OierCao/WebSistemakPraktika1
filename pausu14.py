import requests
import time
import random

# Zure ThingSpeak kanalaren Write API Key
CHANNEL_API_KEY = 'RVNPYS0U7ZX42F7J'

# Datuak igotzeko funtzioa
def upload_data(balio1, balio2):
    metodoa = 'POST'
    url = 'https://api.thingspeak.com/update.json'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'api_key': CHANNEL_API_KEY,
        'field1': balio1,
        'field2': balio2
    }

    response = requests.request(metodoa, url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"Datuak ondo igota: field1 {balio1}, field2 {balio2}")
    else:
        print("Errorea datuak igotzean")


if __name__ == "__main__":
    while True:
        balio1 = 15
        balio2 = 20
        upload_data(balio1, balio2)

        time.sleep(15)
