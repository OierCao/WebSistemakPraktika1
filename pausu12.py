import requests
import urllib.parse
import json

USER_API_KEY = "MCIGO5M0K4O6WGTF"
def create_channel():
   metodoa = 'POST'
   uria = "https://api.thingspeak.com/channels.json"
   goiburuak = {'Host': 'api.thingspeak.com',
                'Content-Type': 'application/x-www-form-urlencoded'}
   edukia = {'api_key': USER_API_KEY,
             'name': 'Nire kanala',
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
   edukia = erantzuna.content
   print(edukia)


   jsonLoad = json.loads(edukia)
   id = str(jsonLoad['id'])


   apiKey = None
   for key in jsonLoad['api_keys']:
       if key['write_flag']:
           apiKey = key['api_key']
           break


   with open("pausu12.txt", 'w') as file:
       if apiKey is not None:
           file.write("id: " + id + " eta Api Key Write:" + apiKey)
       else:
           file.write('Ez da aurkitu WRITE_API_KEY')


if __name__ == "__main__":
   print("Creating channel...")
   create_channel()
   print("Channel created. Check on ThingSpeak")