from dataclasses import dataclass
import locale

import click
import desert
import marshmallow
import requests


@dataclass
class Page:
    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(language: str = "local") -> Page:
    if language == "local":
        # Recognize current language with locale
        # first part of locale language code e.g. 'pl_PL'
        language = locale.getlocale()[0].split("_")[0]

    api_url: str = f"https://{language}.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as err:
        msg = f"Wikipedia API is not reachable: {str(err)}"
        raise click.ClickException(msg) from None
