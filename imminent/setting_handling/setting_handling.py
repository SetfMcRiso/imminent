import os
import json
from pathlib import Path


class JSON():

    """
    Class to handle the JSON Files
    """

    def __init__(self, filepath):
        """
        Initialization of the object
        @filepath       full path of the Settings file
        """
        self.values = dict()
        self.filepath = filepath
        if not os.path.isfile(filepath):
            template = self._get_template()
            with open(filepath, 'w', encoding='utf-8') as fil:
                json.dump(template, fil,
                          ensure_ascii=False, indent=4)

    def _get_template(self):
        return {}

    def _load_values(self):
        try:
            with open(self.filepath) as json_file:
                values = json.load(json_file)
        except Exception as ex:
            raise ex
        return values

    def load_setting(self):
        """
        Loads the information of the Settings file in a class attribute
        self.values which is a dictionary.
        """
        self.values = self._load_values()
        return isinstance(self.values, dict)

    def save_setting(self):
        """
        Saves the information of the self.values to the file
        if the information is valid
        """
        with open(self.filepath, 'w+', encoding='utf-8') as fil:
            json.dump(self.values, fil, ensure_ascii=False, indent=4)
        return True

    def _has_dict_value(self, dictionary, attribute_list):
        value = None
        found = False
        if isinstance(attribute_list, list):
            attribute = attribute_list[0]
            next_attribute = attribute_list[1:]
        else:
            attribute = attribute_list
            next_attribute = []
        if isinstance(dictionary, dict) \
                and attribute in dictionary.keys():
            value = dictionary[attribute]
            found = True
        elif isinstance(dictionary, list)\
                and isinstance(attribute, int)\
                and len(dictionary) > attribute:
            value = dictionary[attribute]
            found = True
        if next_attribute == []:
            return found
        return (value is not None and
                self._has_dict_value(value, next_attribute))

    def _get_dict_value(self, dictionary, attribute_list):
        value = None
        if isinstance(attribute_list, list):
            attribute = attribute_list[0]
            next_attribute = attribute_list[1:]
        else:
            attribute = attribute_list
            next_attribute = []
        if isinstance(dictionary, dict) \
                and attribute in dictionary.keys():
            value = dictionary[attribute]
        elif isinstance(dictionary, list)\
                and isinstance(attribute, int)\
                and len(dictionary) > attribute:
            value = dictionary[attribute]
        if next_attribute == []:
            return value
        return self._get_dict_value(value, next_attribute)

    def get_value(self, attribute_path):
        """
        Gets the value of the requested attribute.
        @attribute_path: list of the keys in the dictionary from root to leaf
        """
        return self._get_dict_value(self.values, attribute_path)


if __name__ == "__main__":
    mitsos = JSON(os.path.join(
        Path(__file__).parents[0], 'test.json'))
    mitsos.load_setting()
    print(mitsos.get_value(['id']))
