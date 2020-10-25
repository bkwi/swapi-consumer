from functools import lru_cache

from django.conf import settings

import requests
import petl as etl


FIELDS_WE_GET = [
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
    'edited',
]

FIELDS_WE_NEED = FIELDS_WE_GET[:-2] + ['date']


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

    etl.tocsv([FIELDS_WE_NEED], filepath)

    while addr:
        response = requests.get(addr).json()
        addr = response['next']

        table_columns = [
            [
                item[column_name] for item in response['results']
            ] for column_name in FIELDS_WE_GET
        ]

        table = (
            etl.fromcolumns(table_columns, header=FIELDS_WE_GET)
            .convert('homeworld', resolve_homeworld)
            .addfield('date', lambda rec: rec['edited'].split('T')[0])
            .cutout('created')
            .cutout('edited')
        )

        etl.appendcsv(table, filepath)


def load_more(filepath, length=10, offset=0):
    table = etl.fromcsv(filepath)
    rows = etl.rowslice(table, offset, length).dicts()
    return etl.header(table), list(rows)
