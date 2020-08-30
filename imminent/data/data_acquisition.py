import subprocess
import json
import os
import ast
from pathlib import Path
from imminent.setting_handling.setting_handling import JSON


class Data():
    """
    Class that is handling the data acquisition.
    """

    def __init__(self):
        pass

    def _execute_command(self, cmd, cwd=None):
        self._last_cmd = cmd
        try:
            out = subprocess.check_output(self._last_cmd, cwd=cwd,
                                          shell=True, universal_newlines=True,
                                          stderr=subprocess.STDOUT)
            return out
        except subprocess.CalledProcessError as ex:
            self._error(
                "Fail {}/\n when calling command '{}'.".format(cmd, ex))
            return -1


if __name__ == "__main__":
    out = Data()._execute_command('curl -H "Authorization: Bearer USRVbibiAyyHQHSbjqa7Cafn66ho8fJ0A0" https://eu.api.blizzard.com/profile/wow/character/twisting-nether/kugarina/character-media?namespace=profile-eu')
    mitsos = ast.literal_eval(out.splitlines()[-1])
    mitsaras = JSON(os.path.join(Path(__file__).parents[0], 'test.json'))
    mitsaras.values = mitsos
    mitsaras.save_setting()
    print(mitsos)
    print(type(mitsos))
