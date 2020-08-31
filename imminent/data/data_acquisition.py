import subprocess
import json
import os
import ast
from pprint import pprint
from pathlib import Path
from imminent.setting.setting_handling import JSON
from requests_oauthlib import OAuth2Session
import requests


class Data():
    """
    Class that is handling the data acquisition.
    """

    def __init__(self, name=None, realm=None):
        self.name = name
        self.realm = realm

    def get_access_token(self):
        client_id = self._get_client_id()
        client_secret = self._get_client_secret()
        token_url = 'https://us.battle.net/oauth/token'
        grant_type = 'client_credentials'
        body_params = {'grant_type': grant_type}
        response = requests.post(token_url, data=body_params,
                                 auth=(client_id, client_secret))
        token_raw = json.loads(response.text)
        print(token_raw)
        return token_raw["access_token"]

    def _get_client_id(self):
        return '966c2753943b44988942d3faf60db027'

    def _get_client_secret(self):
        return 'WCSEYp0Ks75J7xDtoIHHgCX8wkS1D4cX'


if __name__ == "__main__":
    token = Data().get_access_token()
    print(token)
    headers = {"Authorization": "Bearer {}".format(token)}
    r = requests.get(
        url="https://eu.api.blizzard.com/profile/wow/character/twisting-nether/kugarina/equipment?namespace=profile-eu&locale=en_GB", headers=headers)
    resp = json.loads(r.text)
    pprint(resp)
    print(len(resp))
