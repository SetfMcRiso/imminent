import subprocess
import json
import os
import ast
from pathlib import Path
from datetime import datetime
from imminent.setting.setting_handling import JSON
from imminent.utilities.file_handling import ResourceHandler
from imminent.utilities.file_handling import FileHandler
import requests

enchant_list = ['FINGER_1',
                'FINGER_2',
                'MAIN_HAND',
                'OFF_HAND']


class Data():
    """
    Class that is handling the data acquisition.
    """

    def __init__(self, name=None, realm=None):
        self.name = name
        self.realm = realm
        self.base_url = 'https://eu.api.blizzard.com/profile/wow/character/'
        self.base_url += f'{realm}/{name}'
        self._tmp_dir = os.path.join(
            Path.home(),
            'Imminent',
            name + '_' + realm)

    def get_access_token(self):
        """
        Gets the access token needed for OAuth2
        """
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
        """
        Downloads the data requested in the C://Users/currentuser/Imminent
        The folder Imminent and the individual character folders are created
        """
        FileHandler().make_directory(self._tmp_dir)
        path = os.path.join(self._tmp_dir, category + '.json')
        file = JSON(path)
        url = self._get_url(category)
        response = self._request_data(url)
        file.values = json.loads(response.text)
        file.save_setting()

    def _get_info(self, category, attribute_list):
        """
        Returns the character information given from the attribute list
        in the (category).json file.
        Requires the (category).json file to have already be downloaded.
        """
        path = os.path.join(self._tmp_dir, category + '.json')
        file = JSON(path)
        file.load_setting()
        return file.get_value(attribute_list)

    def get_class(self):
        """
        Returns the character's class.
        Requires the character.json file to have already be downloaded
        """
        return self._get_info('character', ['character_class', 'name'])

    def get_active_spec(self):
        """
        Returns the character's class spec.
        Requires the character.json file to have already be downloaded
        """
        return self._get_info('character', ['active_spec', 'name'])

    def get_max_ilvl(self):
        """
        Returns the character's highest ilvl.
        Requires the character.json file to have already be downloaded
        """
        return self._get_info('character', ['average_item_level'])

    def get_equipped_ilvl(self):
        """
        Returns the character's equipped ilvl.
        Requires the character.json file to have already be downloaded
        """
        return self._get_info('character', ['equipped_item_level'])

    def get_last_online(self):
        """
        Returns the character's last login.
        Requires the character.json file to have already be downloaded
        """
        timestamp = self._get_info('character', ['last_login_timestamp'])/1000
        return datetime.utcfromtimestamp(timestamp)

    def get_socket_count(self):
        """
        Returns the character's socket count.
        Requires the equipment.json file to have already be downloaded
        """
        socket_counter = 0
        equipment_dictionary = self._get_info('equipment', ['equipped_items'])
        for _ in equipment_dictionary:
            if 'sockets' in _.keys():
                socket_counter += 1
        return socket_counter

    def get_non_enchanted_items(self):
        """
        Returns a list of the character's non enchanted items.
        Requires the equipment.json file to have already be downloaded
        """
        missing_enchants_list = []
        equipment_dictionary = self._get_info('equipment', ['equipped_items'])
        for _ in equipment_dictionary:
            if _['slot']['type'] in enchant_list:
                if 'enchantments' not in _.keys():
                    missing_enchants_list.append(_['slot']['type'])
        return missing_enchants_list


if __name__ == "__main__":
    kugar = Data('kugarina', 'twisting-nether')
    kugar.download_data('equipment')
    print(kugar.get_non_enchanted_items())
