import requests
import urllib

USER_API_KEY = 'MCIGO5M0K4O6WGTF'

def kanala_hustu(channelID):
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
    deskribapena = erantzuna.reason
    print("Kanala hustu:")
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

if __name__ == '__main__':
    kanala_hustu('2436265')
