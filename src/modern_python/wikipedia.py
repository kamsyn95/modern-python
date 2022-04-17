import locale

import click
import requests


def random_page(language='local'):
    if language == 'local':
        # Recognize current language with locale
        # first part of locale language code e.g. 'pl_PL'
        language = locale.getlocale()[0].split('_')[0]

    api_url = f"https://{language}.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as err:
        msg = f'Wikipedia API is not reachable: {str(err)}'
        raise click.ClickException(msg)
