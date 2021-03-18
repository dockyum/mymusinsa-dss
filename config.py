import configparser
import os


config_file = os.path.join(os.path.dirname(__file__), 'datas.ini')

config = configparser.ConfigParser()
config.read(config_file)
mymms = config["mymusinsa"]

class Config(object):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    DATABASE_URL = mymms["DATABASE_URL"]