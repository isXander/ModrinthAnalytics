import json

import requests
from types import SimpleNamespace
from labrinth.api import *


def user(user, token):
    response = requests.get(f'{url}/user/{user}', auth=(token, ''))
    return response.json(object_hook=lambda d: SimpleNamespace(**d))


def projects(user: str, token):
    response = requests.get(f'{url}/user/{user}/projects', auth=(token, ''))
    try:
        return response.json(object_hook=lambda d: SimpleNamespace(**d))
    except json.decoder.JSONDecodeError:
        print(f"Couldn't decode JSON: {response.text}")


