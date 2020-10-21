from django.conf import settings

import requests


def fetch_collection():
    people = []
    addr = f'{settings.SWAPI_HOST}/api/people'
    while addr:
        response = requests.get(addr).json()
        addr = response['next']
        people.extend(response['results'])
