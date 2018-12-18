import os
import configparser


"""This holds configuration information for Kingfisher.
Whatever tool is calling it - CLI or other code - should create one of these, set it up as required and pass it around.
"""


class Config:

    def __init__(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        # This sets the default base dir in the code folder. There is an issue to change this later.
        # https://github.com/open-contracting/kingfisher/issues/223
        self.data_dir = os.path.join(this_dir, "..", "data")
        # Some hard coded defaults that should default to blank and be loaded properly TODO
        self.server_url = 'http://localhost:9090'
        self.server_api_key = 'cat'

    def load_user_config(self):
        # First, try and load any config in the ini files
        self._load_user_config_ini()
        # Second, try and load any config in the env (so env overwrites ini)
        self._load_user_config_env()

    def _load_user_config_env(self):
        if os.environ.get('KINGFISHER_DATA_DIR'):
            self.data_dir = os.environ.get('KINGFISHER_DATA_DIR')

    def _load_user_config_ini(self):

        config = configparser.ConfigParser()

        if os.path.isfile(os.path.expanduser('~/.config/ocdskingfisher/config.ini')):
            config.read(os.path.expanduser('~/.config/ocdskingfisher/config.ini'))
        elif os.path.isfile(os.path.expanduser('~/.config/ocdsdata/config.ini')):
            config.read(os.path.expanduser('~/.config/ocdsdata/config.ini'))
        else:
            return

        self.data_dir = config.get('DATA', 'DIR', fallback=self.data_dir)
