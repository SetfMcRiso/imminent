import scrapy
import json
import subprocess
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from imminent.utilities.file_handling import FileHandler
from imminent.setting.setting_handling import JSON

dungeons = {
    'junkyard' 		: 800001,
    'freehold' 		: 9164,
    'underrot' 		: 9391,
    'tol_dagor' 	: 9327,
    'atal_dazar'	: 9028,
    'shrine'		: 9525,
    'workshop'		: 800002,
    'motherload'	: 8064,
    'sethraliss'	: 9527,
    'manor'			: 9424,
    'boralus'		: 9354,
    'kings_rest'	: 9526
}


class RioScrapingSpider(scrapy.Spider):

    name = 'rio_scraping'

    def __init__(self, char_name, realm_slug, region, **kwargs):
        self.char_name = char_name
        self.realm_slug = realm_slug
        self.region = region
        self.tmp_dir = os.path.join(
            Path.home(),
            'Imminent',
            char_name + '_' + realm_slug,
            'mythic_plus')
        self.start_urls = [
            f'https://raider.io/characters/{region}/{realm_slug}/{char_name}']
        self.char_id = RioCharacterId(
            char_name, realm_slug, region).get_char_id()
        super().__init__(**kwargs)

    def parse(self, response):
        for _ in dungeons.keys():
            url = 'https://raider.io/api/characters' +\
                '/mythic-plus-runs?season=' +\
                f'season-bfa-4&characterId={self.char_id}' +\
                f'&dungeonId={dungeons[_]}&role' +\
                '=all&specId=0&mode=scored&affixes=all&date=all'
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-AU,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7" +
                ",fr-FR;q=0.6,fr;q=0.5,en-GB;q=0.4,en-US;q=0.3,el;q=0.2" +
                ",de;q=0.1,ru;q=0.1",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "referer": f"https://raider.io/characters/{self.region}" +
                f"/{self.realm_slug}/{self.char_name}",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
                " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183" +
                ".102 Safari/537.36"
            }
            yield scrapy.Request(url, callback=self.parse_api, headers=headers)

    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        if len(data['runs']) != 0:
            dungeon_id = data['runs'][0]["summary"]["dungeon"]["id"]
            dungeon_name = self._get_dungeon_name(dungeon_id)
            self._save_info(dungeon_name, data)

    def _get_dungeon_name(self, id):
        for _ in dungeons.keys():
            if dungeons[_] == id:
                return _

    def _save_info(self, dungeon_name, data):
        FileHandler().make_directory(self.tmp_dir)
        path = os.path.join(self.tmp_dir, dungeon_name+'.json')
        file = JSON(path)
        file.values = data
        file.save_setting()


class RioCharacterId():

    def __init__(self, char_name, realm_slug, region):
        url = f'https://raider.io/characters/{region}/{realm_slug}/{char_name}'
        source = requests.get(url).text
        self.soup = BeautifulSoup(source, 'lxml')

    def get_char_id(self):
        meta = self.soup.find(
            'meta', {'data-react-helmet': "true", "property": "og:image"})
        return str(meta).split('/')[6]


if __name__ == "__main__":
    mitsos = RioCharacterId('Kugaroula', 'twisting-nether', 'eu')
    print(mitsos.get_char_id())
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(RioScrapingSpider, char_name='Nemiu',
                  realm_slug='twisting-nether', region='eu')
    process.start()
