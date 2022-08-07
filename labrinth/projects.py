import requests
from types import SimpleNamespace
from labrinth.api import *


def project(id_or_slug, token):
    response = requests.get(f'{url}/project/{id_or_slug}', auth=(token, ''))
    return response.json(object_hook=lambda d: SimpleNamespace(**d))
