"""Client for the Wikipedia REST API, version 1.

See `API documentation <https://en.wikipedia.org/api/rest_v1/#/>`_.
"""
from dataclasses import dataclass
import locale

import click
import desert
import marshmallow
import requests


@dataclass
class Page:
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page.
        extract: A plain text summary.
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(language: str = "local") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        language: The Wikipedia language edition. By default,
            language recognized by locale is used ("local").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    Example:
        >>> from modern_python import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    if language == "local":
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
