import subprocess
import json
import os
import ast
from pathlib import Path
from imminent.setting.setting_handling import JSON
from imminent.utilities.file_handling import ResourceHandler
from imminent.utilities.file_handling import FileHandler
import requests


class Data():
    """
    Class that is handling the data acquisition.
    """

    def __init__(self, name=None, realm=None):
        self.name = name
        self.realm = realm
        self.base_url = 'https://eu.api.blizzard.com/profile/wow/character/'
        self.base_url += f'{realm}/{name}/'
        self._tmp_dir = os.path.join(
            Path.home(),
            'Imminent',
            name + '_' + realm)

    def get_access_token(self):
        client_id = self._get_client_id()
        client_secret = self._get_client_secret()
        token_url = 'https://us.battle.net/oauth/token'
        grant_type = 'client_credentials'
        body_params = {'grant_type': grant_type}
        response = requests.post(token_url, data=body_params,
                                 auth=(client_id, client_secret))
        token_raw = json.loads(response.text)
        return token_raw["access_token"]

    def _get_client_id(self):
        client_path = ResourceHandler().get_resource('client.json')
        client = JSON(client_path)
        client.load_setting()
        return client.get_value('id')

    def _get_client_secret(self):
        client_path = ResourceHandler().get_resource('client.json')
        client = JSON(client_path)
        client.load_setting()
        return client.get_value('secret')

    def _get_header(self):
        token = self.get_access_token()
        header = {"Authorization": "Bearer {}".format(token)}
        return header

    def _request_data(self, url):
        headers = self._get_header()
        response = requests.get(url=url, headers=headers)
        return response

    def _get_url(self, category):
        url_path = ResourceHandler().get_resource('urls.json')
        url = JSON(url_path)
        url.load_setting()
        url_part = url.get_value(category)
        if url_part is not None:
            url_part += '?namespace=profile-eu&locale=en_GB'
            return self.base_url + url_part
        return None

    def download_data(self, category):
        FileHandler().make_directory(self._tmp_dir)
        path = os.path.join(self._tmp_dir, category + '.json')
        file = JSON(path)
        url = self._get_url(category)
        response = self._request_data(url)
        file.values = json.loads(response.text)
        file.save_setting()


if __name__ == "__main__":
    kugar = Data('kugartwo', 'twisting-nether')
    kugar.download_data('quests')
