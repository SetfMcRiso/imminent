import scrapy
import json
import subprocess
import requests
import os
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
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

    def __init__(self, char_list, guild, ** kwargs):
        self.char_name = ''
        self.realm_slug = ''
        self.region = ''
        self.guild = guild
        self.tmp_dir = os.path.join(
            Path.home(),
            'Kugar\'s Guild Management Tool',
            self.guild)
        self.char_list = char_list
        self.start_urls = [
            f'https://raider.io/']
        self.char_id = 0
        super().__init__(**kwargs)

    def start_requests(self):
        for char in self.char_list:
            self.char_id = RioCharacterId(
                char[0], char[1], char[2]).get_char_id()
            print(self.char_id, char)
            self.char_name = char[0]
            self.realm_slug = char[1]
            self.region = char[2]
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
                    "referer": f"https://raider.io/characters/{char[2]}" +
                    f"/{char[1]}/{char[0]}",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
                    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome" +
                    "/85.0.4183.102 Safari/537.36"
                }
                yield scrapy.Request(url, callback=self.parse,
                                     headers=headers,
                                     meta={'char_name': char[0],
                                           'realm_slug': char[1]})

    def parse(self, response):
        char_name = response.meta.get('char_name')
        realm_slug = response.meta.get('realm_slug')
        raw_data = response.body
        data = json.loads(raw_data)
        if len(data['runs']) != 0:
            dungeon_id = data['runs'][0]["summary"]["dungeon"]["id"]
            dungeon_name = self._get_dungeon_name(dungeon_id)
            self._save_info(dungeon_name, data, char_name, realm_slug)

    def _get_dungeon_name(self, id):
        for _ in dungeons.keys():
            if dungeons[_] == id:
                return _

    def _save_info(self, dungeon_name, data, char_name, realm_slug):
        path = os.path.join(
            Path.home(),
            'Kugar\'s Guild Management Tool',
            self.guild,
            char_name + '_' + realm_slug,
            'mythic_plus')
        FileHandler().make_directory(path)
        path = os.path.join(path, dungeon_name+'.json')
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
    mitsos = RioCharacterId('kugaroula', 'twisting-nether', 'eu')
    print(mitsos.get_char_id())
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    char_list = [('kugarina', 'twisting-nether', 'eu'),
                 ('kugaroula', 'twisting-nether', 'eu')]
    process.crawl(RioScrapingSpider, char_list, 'Imminent')
    process.start()
    '''
     for _ in range(2):
                   run_spider(RioScrapingSpider, char_name='Nemiu',
                   realm_slug='twisting-nether',
                   guild='Imminent', region='eu') '''
    """
    , char_name='Nemiu',
                   realm_slug='twisting-nether', guild='Imminent', region='eu'
    """
