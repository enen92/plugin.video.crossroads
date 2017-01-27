import requests


# Streamspot
_streamspot_url = 'https://api.streamspot.com/'
_streamspot_api_key = 'a0cb38cb-8146-47c2-b11f-6d93f4647389'
_streamspot_ssid = 'crossr30e3'
_streamspot_header = {
    "Content-Type": 'application/json',
    "x-API-Key": _streamspot_api_key
}
_streamspot_player = '2887fba1'

resp = requests.get('{}broadcaster/{}?players=true'.format(_streamspot_url, _streamspot_ssid), headers=_streamspot_header)
data = resp.json()['data']
print data