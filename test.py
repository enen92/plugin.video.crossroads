import json
import requests
import datetime
# Streamspot
_streamspot_url = 'https://api.streamspot.com/'
_streamspot_api_key = 'a0cb38cb-8146-47c2-b11f-6d93f4647389'
_streamspot_ssid = 'crossr30e3'
_streamspot_header = {
    "Content-Type": 'application/json',
    "x-API-Key": _streamspot_api_key
}
_now = datetime.datetime.now()

def isBroadcasting(event):
    return datetime.datetime.strptime(event['start'], "%Y-%m-%d %H:%M:%S") < _now and datetime.datetime.strptime(event['end'], "%Y-%m-%d %H:%M:%S") > _now

def isUpcoming(event):
    return datetime.datetime.strptime(event['start'], "%Y-%m-%d %H:%M:%S") > _now

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

resp = requests.get("{}broadcaster/{}/events".format(_streamspot_url, _streamspot_ssid),
                    headers=_streamspot_header)
data = resp.json()['data']['events']

cur_events = []

for stream in data:
    if isUpcoming(stream) or isBroadcasting(stream):
        cur_events.append(stream)

print(cur_events)
