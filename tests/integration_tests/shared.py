import requests


def post_to(route):
    return requests.post(f'http://localhost:5000/{route}', {}).text
