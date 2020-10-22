from functools import lru_cache

from django.conf import settings

import requests
import petl as etl


FIELDS = [
    'name',
    'height',
    'mass',
    'hair_color',
    'skin_color',
    'eye_color',
    'birth_year',
    'gender',
    'homeworld',
    'created',
    'edited'
]


@lru_cache()
def resolve_homeworld(url):
    """
    Get homeworld name from given url.
    Use lru_cache to aviod multiple requests for the same resource
    """
    response = requests.get(url).json()
    return response['name']


def fetch_collection(filepath):
    addr = f'{settings.SWAPI_HOST}/api/people'

    headers = [FIELDS]
    etl.tocsv(headers, filepath)

    while addr:
        response = requests.get(addr).json()
        addr = response['next']

        table_columns = [
            [
                item[column_name] for item in response['results']
            ] for column_name in FIELDS
        ]

        table = (
            etl.fromcolumns(table_columns, header=FIELDS)
            .convert('homeworld', resolve_homeworld)
            .addfield('date', lambda rec: rec['edited'].split('T')[0])
        )
        etl.appendcsv(table, filepath)
