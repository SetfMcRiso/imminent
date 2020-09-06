import os
import logging
from pathlib import Path
import pkgutil

_LOGGER = logging.getLogger('imminent.file_handling')


class FileHandler():
    """
    Class to handle files and folders.
    example code to initiate this class:
        Create instance of this class
        filehandler = FileHandler()
    """
    @classmethod
    def make_directory(cls, folder_path):
        """
        Method to create a folder by its absolut path.
        @folder_path         full path of the folder.
        example code to call this method:
            FileHandler.make_directory('folder_path')
        """
        if not os.path.exists(folder_path):
            try:
                _LOGGER.info(f'Creating the following '
                             + f'directory: {folder_path}')
                os.makedirs(folder_path)
            except Exception as ex:
                _LOGGER.error(
                    'No rights to create the directory: %s', folder_path)
                raise ex
        return True


class ResourceHandler():

    """
    Class to handle the installed data files
    """

    def __init__(self):
        self._tmp_dir = os.path.join(
            Path.home(),
            'Temporary')

    def get_resource(self, resource_name):
        """
        Returns the path of the required resource file
        @resource_name       name of the resource file
                            (only the name, not the full path)
        """
        resource_path = self._get_data(resource_name)
        if resource_path is not None:
            _LOGGER.info(f'Installed data file found : {resource_path}')
            return resource_path
        resource_path = os.path.join(Path(__file__).parents[1],
                                     'resources',
                                     resource_name)
        _LOGGER.info(f'Installed data file not found'
                     + f'returning the resource folder path : {resource_path}')
        return os.path.join(Path(__file__).parents[1],
                            'resources',
                            resource_name)

    def _get_data(self, filename):
        """
        Returns the path of the copied decoded file
        or None if the file does not exist
        @filename       name of the resource file
                        (only the name, not the full path)
        """
        try:
            self._create_temp_dir()
            data = pkgutil.get_data('athena', filename).decode(
                'UTF-8', 'ignore')
            filepath = os.path.join(self._tmp_dir, filename)
            with open(filepath, 'w') as file:
                file.write(data)
            return filepath
        except Exception:
            return None

    def _create_temp_dir(self):
        if not os.path.exists(self._tmp_dir):
            FileHandler().make_directory(self._tmp_dir)
