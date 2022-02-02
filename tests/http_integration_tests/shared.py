import requests
import json


def post_to(route, body={}):
    return json.loads(requests.post(f'http://localhost:5000/{route}', json=body).text)
