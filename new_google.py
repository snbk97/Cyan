import requests
import json
from unidecode import unidecode
key = 'YOUR_GOOGLE_API_KEY'
api_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + key


def g_short(url):
    header = {'Content-Type': 'application/json'}
    param = json.dumps({'longUrl': url})
    response = requests.post(api_url, param, headers=header)

    return unidecode(response.json()['id'])
