import json
import requests


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

resp = requests.get('https://www.crossroads.net/proxy/content/api/series')
data = resp.json()['series']
for series in data:
    print('{} {}'.format(series['id'], remove_non_ascii(series['title']))) 


