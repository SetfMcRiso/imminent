import subprocess
import json
import os
import ast
import pytz
from pathlib import Path
import requests
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from imminent.setting.setting_handling import JSON
from imminent.utilities.file_handling import ResourceHandler
from imminent.utilities.file_handling import FileHandler
from imminent.data.rio_scraping import RioScrapingSpider

enchant_list = ['FINGER_1',
                'FINGER_2',
                'MAIN_HAND',
                'OFF_HAND']
shadowlands_release_timestamp = 1603753200
bfa_timestamp = 1577836800
test_timestamp = 1598914800


class Data():
    """
    Class that is handling the data acquisition.
    """

    def __init__(self, char_name, realm_slug, guild, region='eu'):
        self.char_name = char_name
        self.realm_slug = realm_slug
        self.region = region
        self.guild = guild
        self.base_url = 'https://eu.api.blizzard.com/profile/wow/character/'
        self.base_url += f'{self.realm_slug}/{self.char_name}'
        self._tmp_dir = os.path.join(
            Path.home(),
            'Kugar\'s Guild Management Tool',
            self.guild,
            self.char_name + '_' + self.realm_slug)
        self._mythic_plus_count_list = []

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

    def _get_reset_timestamp_list(self):
        starting_timestamp = bfa_timestamp
        reset_list = []
        today_weekday = datetime.today().weekday()
        days_from_reset = (today_weekday + 5) % 7
        last_wednesday = datetime.today() - timedelta(days=days_from_reset)
        last_wednesday_string = str(last_wednesday)[0:11:] + '07:00:00'
        last_wednesday_object = datetime.strptime(
            last_wednesday_string, '%Y-%m-%d %H:%M:%S').replace(
                tzinfo=pytz.UTC)
        last_wednesday_timestamp = datetime.timestamp(last_wednesday_object)
        while last_wednesday_timestamp >= starting_timestamp:
            reset_list.append(last_wednesday_timestamp)
            last_wednesday_object = last_wednesday_object - timedelta(days=7)
            last_wednesday_timestamp = datetime.timestamp(
                last_wednesday_object)
        return reset_list

    def get_mythic_plus_done_per_week(self):
        """
        Returns the number of mythic plus dungeons completed this reset.
        Requires the mythic_plus.json file to have already be downloaded
        """
        reset_list = self._get_reset_timestamp_list()
        mythic_plus_file_list = self._get_list_of_all_mythic_plus_files()
        self._mythic_plus_count_list = [0]*len(reset_list)
        for file in mythic_plus_file_list:
            self._update_mythic_plus_count_list(reset_list, file)
        return self._mythic_plus_count_list

    def _update_mythic_plus_count_list(self, reset_list, filename):
        file = JSON(filename)
        file.load_setting()
        for _ in file.values['runs']:
            run_completion_time = datetime.strptime(
                _['summary']['completed_at'][:-5:],
                '%Y-%m-%dT%H:%M:%S').replace(
                tzinfo=pytz.UTC)
            run_completion_timestamp = datetime.timestamp(run_completion_time)
            counter = self._get_mythic_plus_week_from_timestamp(
                reset_list, run_completion_timestamp)
            if counter is not False:
                self._mythic_plus_count_list[counter] += 1

    def _get_mythic_plus_week_from_timestamp(
            self, reset_list, run_completion_timestamp):
        if run_completion_timestamp < reset_list[-1]:
            return False
        for _ in range(0, len(reset_list)):
            if reset_list[_] < run_completion_timestamp:
                return _

    def get_mythic_rewards_this_reset(self):
        """
        Returns a list with the mythic plus items for the current reset
        """
        return self._get_mythic_rewards(0)

    def _get_mythic_rewards(self, reset):
        reset_list = self._get_reset_timestamp_list()
        mythic_plus_file_list = self._get_list_of_all_mythic_plus_files()
        completed_keys_list = []
        rewards_list = [0]*3
        for _ in mythic_plus_file_list:
            completed_keys_list += self._get_list_of_mythic_plus_per_dungeon(
                _, reset_list, reset)
        completed_keys_list.sort(reverse=True)
        if len(completed_keys_list) != 0:
            rewards_list[0] = completed_keys_list[0]
        if len(completed_keys_list) >= 4:
            rewards_list[1] = completed_keys_list[3]
        if len(completed_keys_list) >= 10:
            rewards_list[2] = completed_keys_list[9]
        return rewards_list

    def _get_list_of_mythic_plus_per_dungeon(
            self, filename, reset_list, reset):
        file = JSON(filename)
        file.load_setting()
        completed_keys_list = []
        for _ in file.values['runs']:
            run_completion_time = datetime.strptime(
                _['summary']['completed_at'][:-5:],
                '%Y-%m-%dT%H:%M:%S').replace(
                tzinfo=pytz.UTC)
            run_completion_timestamp = datetime.timestamp(run_completion_time)
            if run_completion_timestamp > reset_list[reset]:
                completed_keys_list.append(_['summary']['mythic_level'])
        return completed_keys_list

    def _get_list_of_all_mythic_plus_files(self):
        directory = os.path.join(self._tmp_dir, 'mythic_plus')
        file_list = []
        filenames = os.listdir(directory)
        for _ in filenames:
            file_list.append(os.path.join(directory, _))
        return file_list

    def download_mythic_plus_data(self):
        process = CrawlerProcess()
        process.crawl(RioScrapingSpider, char_name=self.char_name,
                      realm_slug=self.realm_slug, guild=self.guild,
                      region=self.region)
        process.start()


if __name__ == "__main__":
    # print(os.listdir(r'C:\Users\stefm\Imminent\kugarina_twisting-nether\mythic_plus'))
    kugar = Data('Curvajal', 'twisting-nether', 'Imminent 2')
    kugar.download_mythic_plus_data()
    print(kugar._get_mythic_rewards(0))
