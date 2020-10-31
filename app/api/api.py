#!/usr/bin/python3

import requests
from requests.exceptions import HTTPError, Timeout, RequestException, TooManyRedirects
from os import getenv

class ApiConnector:

    http = None

    headers = {}

    def __init__(self):
        self.http = requests
        self.load_headers()


    def get(self, url: str):
        try:
            req = self.http.get(url, headers=self.headers)
            if req.status_code == 200 or req.status_code == 201:
                return req.json()
            else:
                return None
        except (ConnectionError, Timeout, HTTPError, RequestException):
            return None

    def post(self, url: str, data: dict):
        try:
            req = self.http.post(url, headers=self.headers, data=data)
            if req.status_code == 200 or req.status_code == 201:
                return req.json()
            else:
                return None
        except (ConnectionError, Timeout, HTTPError, RequestException):
            return None

    def load_headers(self):
        self.headers['Authorization'] = 'Bearer {token}'.format(
            token=getenv('API_TOKEN')
        )
        self.headers['Content-Type'] = 'application/json'