from functools import lru_cache
from django.conf import settings

import requests


@lru_cache()
def resolve_homeworld(url):
    response = requests.get(url).json()
    return response['name']


def fetch_collection():
    people = []
    addr = f'{settings.SWAPI_HOST}/api/people'

    while addr:
        response = requests.get(addr).json()
        addr = response['next']
        for item in response['results']:
            item['homeworld'] = resolve_homeworld(item['homeworld'])
            people.append(item)

    print(people[0])
