from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from pathlib import Path
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from imminent.data.data_acquisition import Data
from imminent.setting.setting_handling import JSON
from imminent.data.rio_scraping import RioScrapingSpider


class GSheetsHandler():

    def __init__(self, parent, json_keyfile, sheet_name, guild):
        self.guild = guild
        self.scope = ["https://spreadsheets.google.com/feeds",
                      "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file",
                      "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open("Imminent")
        self.worksheet1 = self.sheet.sheet1
        self.worksheet1.clear()
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {"updateCells": {
                    "range": {
                        "sheetId": self.worksheet1._properties['sheetId']
                    },
                    "fields": "*"}
                 }
            ]
        }
        self.sheet.batch_update(body)
        body = {
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",
                        "length": 50
                    }
                }
            ]
        }
        if self.worksheet1.col_count < 30:
            self.sheet.batch_update(body)

    def _merge_cells(self, start_row_index, end_row_index,
                     start_column_index, end_column_index):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "mergeCells": {
                        "mergeType": "MERGE_ALL",
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": start_row_index,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": start_column_index,
                            "endColumnIndex": end_column_index
                        }
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def merge_refreshed_cells(self):
        return self._merge_cells(0, 2, 0, 2)

    def merge_itel_level_cells(self):
        return self._merge_cells(0, 1, 4, 6)

    def merge_enchant_cells(self):
        return self._merge_cells(0, 1, 6, 15)

    def merge_reputation_cells(self):
        return self._merge_cells(0, 1, 15, 19)

    def merge_mythic_plus_cells(self):
        return self._merge_cells(0, 1, 19, 22)

    def merge_weekly_rewards_cells(self):
        return self._merge_cells(0, 1, 22, 28)

    def merge_profession_cells(self):
        return self._merge_cells(0, 1, 28, 30)

    def add_borders(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 2,
                            "endColumnIndex": 3
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 15,
                            "endColumnIndex": 16
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 1,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 50
                        },
                        "bottom": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 2,
                            "endRowIndex": 3,
                            "startColumnIndex": 0,
                            "endColumnIndex": 2
                        },
                        "top": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 4,
                            "endColumnIndex": 5
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 6,
                            "endColumnIndex": 7
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 19,
                            "endColumnIndex": 20
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 22,
                            "endColumnIndex": 23
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 28,
                            "endColumnIndex": 29
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                },
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 30,
                            "endColumnIndex": 31
                        },
                        "left": {
                            "style": "SOLID_THICK",
                            "width": 3,
                            "color": {
                                "red": 0,
                                "green": 0,
                                "blue": 0
                            },
                        },
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def add_background_color_first_row(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 50
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "MIDDLE",
                                "horizontalAlignment": "CENTER",
                                "backgroundColor": {
                                    "red": 0.450,
                                    "green": 0.450,
                                    "blue": 0.450
                                },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 0,
                                        "green": 0,
                                        "blue": 0
                                    },
                                    "fontFamily": "Roboto",
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 0,
                            "endColumnIndex": 2
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "MIDDLE",
                                "horizontalAlignment": "CENTER",
                                "backgroundColor": {
                                    "red": 0.450,
                                    "green": 0.450,
                                    "blue": 0.450
                                },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 0,
                                        "green": 0,
                                        "blue": 0
                                    },
                                    "fontFamily": "Roboto",
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def add_background_color_second_row(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 1,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 50
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "MIDDLE",
                                "horizontalAlignment": "CENTER",
                                "backgroundColor": {
                                    "red": 0.450,
                                    "green": 0.450,
                                    "blue": 0.450
                                },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 0,
                                        "green": 0,
                                        "blue": 0
                                    },
                                    "fontFamily": "Roboto",
                                    "bold": False
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 50,
                            "startColumnIndex": 0,
                            "endColumnIndex": 2
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "MIDDLE",
                                "horizontalAlignment": "CENTER",
                                "backgroundColor": {
                                    "red": 0.450,
                                    "green": 0.450,
                                    "blue": 0.450
                                },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 0,
                                        "green": 0,
                                        "blue": 0
                                    },
                                    "fontFamily": "Roboto",
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def add_first_row_text(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "rows": [
                            {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Last Refreshed " +
                                            str(datetime.now())[:-7:]
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Class"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Item Level"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Enchants"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Reputations"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Mythic Plus Done"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Weekly Rewards"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Proffesions"
                                        }
                                    }
                                ]
                            }
                        ],
                        "fields": "userEnteredValue"
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def add_second_row_text(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": sheetId,
                            "startRowIndex": 1,
                            "endRowIndex": 2
                        },
                        "rows": [
                            {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": ""
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Equipped"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Sockets"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "M.Hand"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "O.Hand"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Cloak"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Chest"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Bracers"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Gloves"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Boots"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Ring 1"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Ring 2"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Ascended"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Wild Hunt"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Undying Army"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Harvesters"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "This Season"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "This Week"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Rio Score"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "M+"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "M+"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "M+"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Raid"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Raid"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Raid"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "First"
                                        }
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Second"
                                        }
                                    }
                                ]
                            }
                        ],
                        "fields": "userEnteredValue"
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def update_dimensions(self):
        sheetId = self.sheet.worksheet('Sheet1')._properties['sheetId']
        body = {
            "requests": [
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'ROWS',
                            'startIndex': 0,
                            'endIndex': 1
                        },
                        'properties': {
                            'pixelSize': 60
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 0,
                            'endIndex': 1
                        },
                        'properties': {
                            'pixelSize': 120
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'ROWS',
                            'startIndex': 1,
                            'endIndex': 2
                        },
                        'properties': {
                            'pixelSize': 30
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 2,
                            'endIndex': 3
                        },
                        'properties': {
                            'pixelSize': 40
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'ROWS',
                            'startIndex': 0,
                            'endIndex': 1
                        },
                        'properties': {
                            'pixelSize': 40
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 4,
                            'endIndex': 6
                        },
                        'properties': {
                            'pixelSize': 70
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 6,
                            'endIndex': 15
                        },
                        'properties': {
                            'pixelSize': 55
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 22,
                            'endIndex': 28
                        },
                        'properties': {
                            'pixelSize': 40
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': sheetId,
                            'dimension': 'COLUMNS',
                            'startIndex': 28,
                            'endIndex': 30
                        },
                        'properties': {
                            'pixelSize': 80
                        },
                        'fields': 'pixelSize'
                    }
                }
            ]
        }
        return self.sheet.batch_update(body)

    def update_char_info(self):
        char_list = self._get_char_list()
        self._run_spider(char_list)

    def download_data(self):
        char_list = self._get_char_list()
        self._download_data(char_list)
        self._update_spreadsheet(char_list)

    def _update_spreadsheet(self, char_list):
        row = 3
        for _ in char_list:
            self.worksheet1.update_cell(row, 1, _[0].capitalize())
            row += 1

    def _run_spider(self, char_list):
        process = CrawlerProcess()
        process.crawl(RioScrapingSpider, char_list, self.guild)
        process.start()

    def _download_data(self, char_list):
        for char in char_list:
            data = Data(char[0], char[1], self.guild, char[2])
            data.download_data()

    def _get_char_list(self):
        char_list = []
        roster_path = os.path.join(
            Path.home(),
            'Kugar\'s Guild Management Tool',
            self.guild,
            'roster',
            'roster.json')
        roster = JSON(roster_path)
        roster.load_setting()
        for _ in roster.values['roster']:
            charname = _.split('/')[7]
            realm_slug = _.split('/')[6]
            region = _.split('/')[5]
            char_list.append((charname, realm_slug, region))
        return char_list

    def generate_report(self):
        self.download_data()
        self.merge_refreshed_cells()
        self.merge_itel_level_cells()
        self.merge_enchant_cells()
        self.merge_reputation_cells()
        self.merge_mythic_plus_cells()
        self.merge_weekly_rewards_cells()
        self.merge_profession_cells()
        self.add_background_color_first_row()
        self.add_background_color_second_row()
        self.add_first_row_text()
        self.add_second_row_text()
        self.update_dimensions()
        self.add_borders()
        self.update_char_info()


if __name__ == "__main__":
    mitsos = GSheetsHandler(
        r'C:\Users\stefm\Downloads\Imminent-b057faf0e02a.json',
        'Imminent', 'Imminent')
    mitsos.merge_refreshed_cells()
    mitsos.merge_itel_level_cells()
    mitsos.merge_enchant_cells()
    mitsos.merge_reputation_cells()
    mitsos.merge_mythic_plus_cells()
    mitsos.merge_weekly_rewards_cells()
    mitsos.merge_profession_cells()
    mitsos.add_background_color_first_row()
    mitsos.add_background_color_second_row()
    mitsos.add_first_row_text()
    mitsos.add_second_row_text()
    mitsos.update_dimensions()
    mitsos.add_borders()
    mitsos.update_char_info()
