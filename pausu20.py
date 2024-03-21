#Ikaslearen izen-abizenak: Oier Cao Carral
#Irakasgaia eta taldea: Web Sistemak, 31
#Entregatze data: 27/02/2024
#Lanaren izena: Laborategi1
#Entregagaiaren deskribapen laburra: 20.pausuaren python programa

import signal
import sys
import urllib.parse
import requests
import json
import psutil
import time
import csv

# Aldagai globalak
USER_API_KEY = "MCIGO5M0K4O6WGTF"
channelID = None
WRITE_API_KEY = None
csvPath = "kanal_datuak_100.csv"

def get_kanal_datuak(json):
    global WRITE_API_KEY
    global channelID

    channelID = str(json["id"])
    for key in json['api_keys']:
        if key['write_flag']:
            WRITE_API_KEY = key['api_key']
            break

def channelExists():
    global channelID  # Ensure you are using the global variable
    metodoa = 'GET'
    uria = f"https://api.thingspeak.com/channels.json?api_key={USER_API_KEY}"
    erantzuna = requests.request(metodoa, uria)
    kodea = erantzuna.status_code

    aurkitua = False
    if kodea == 200:
        kanalak = json.loads(erantzuna.content)
        print(f"Aurkitutako kanal kopurua: {len(kanalak)}")
        for kanal in kanalak:
            print(f"Kanala: {kanal['name']}")  # Debug print
            if kanal['name'] == 'Nire Kanala':
                get_kanal_datuak(kanal)
                aurkitua = True

    if aurkitua:
        print("\n'Nire Kanala' izeneko kanala existitu egiten da jadanik, beraz existitzen den kanala erabiliko dugu.\n")
    else:
        print("\n'Nire Kanala' izeneko kanala ez da exititzen, beraz kanal berri bat sortuko dugu:\n")

    return aurkitua

def create_channel():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': USER_API_KEY,
              'name': 'Nire Kanala',
              'field1': "%CPU",
              'field2': "%RAM"}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    print("\n" + uria)
    print(edukia_encoded)

    erantzuna = requests.request(metodoa, uria, headers=goiburuak,
    data=edukia_encoded, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)

    if kodea == 200:
        jsonDatuak = json.loads(erantzuna.content)
        get_kanal_datuak(jsonDatuak)
        print("Kanala sortua. Begiratu ThingSpeak-en\n")

    elif (kodea == 402):
        print("Kanal kopuru maximora heldu zara!\n")

# Datuak igo
def upload_data(cpu, ram):
    metodoa = 'POST'
    url = 'https://api.thingspeak.com/update.json'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'api_key': WRITE_API_KEY,
        'field1': cpu,
        'field2': ram
    }

    response = requests.request(metodoa, url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"Datuak ondo igota: CPU: %{cpu}, RAM: %{ram}")
    else:
        print("Errorea datuak igotzean")

# Datuak jeitsi eta csv baetan gorde
def csvgorde():
    # Datuak jeitsi
    metodoa = 'GET'
    url = f'https://api.thingspeak.com/channels/{channelID}/feeds.json'
    headers = {'Host': 'api.thingspeak',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'api_key': WRITE_API_KEY,
        'results': '100'
    }

    erantzuna = requests.request(metodoa, url, headers=headers, data=data)
    kodea = erantzuna.status_code

    #csv-an datuak gorde
    if kodea == 200:
        edukia = json.loads(erantzuna.content)
        datuak = edukia['feeds']
        print("Aurkitu diren datu kopurua: " + str(len(datuak)))
        with open(csvPath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['CPU', 'RAM'])
            for datu in datuak:
                cpu = datu['field1']
                ram = datu['field2']
                writer.writerow([cpu, ram])
        print("Datuak gorde egin dira!\n")

# Kanala hustu
def kanala_hustu():
    metodoa = 'DELETE'
    uria = f"https://api.thingspeak.com/channels/{channelID}/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': USER_API_KEY}

    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))

    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code

    if kodea == 200:
        print("'Nire Kanala' izeneko kanala hustu egin da.")


def handler(sig_num, frame):
    # Gertaera kudeatu
    csvgorde()
    kanala_hustu()
    sys.exit(0)

if __name__ == '__main__':
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)

    if not channelExists():
        print("Kanala sortzen...")
        create_channel()

    while True:
        # psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        upload_data(cpu, ram)
        time.sleep(15)

