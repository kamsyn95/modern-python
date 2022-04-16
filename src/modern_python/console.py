import textwrap
import locale

import click
import requests

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern Python project."""

    # Recognize current language with locale
    # first part of locale language code e.g. 'pl_PL'
    lang = locale.getlocale()[0].split('_')[0]
    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"

    try:
        with requests.get(api_url) as response:
            response.raise_for_status()
            data = response.json()
    except requests.exceptions.RequestException as err:
        error_msg = f'Wikipedia API is not reachable\nError: {err}'
        click.secho(error_msg, fg="red")
    else:
        title = data["title"]
        extract = data["extract"]
        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))
