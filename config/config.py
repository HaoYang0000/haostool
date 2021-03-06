"""
This file contains all of the configuration values for the application.
"""
import json
import logging
import os
import platform
from enum import Enum
from app.exceptions.config import ConfigNotFoundException
dir_path = os.path.dirname(os.path.realpath(__file__))
__logger = logging.getLogger(__file__)

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'secret'

# Alternatively, you could use a local MySQL instance for testing.
LOCAL_MYSQL_CONFIG = {
    "address": "localhost",
    "port": 3306,
    "user":"hao",
    "password": "root",
    "database": "personal_tool"
}

LANGUAGES = ['zh_CN', 'en', 'es']

def get_config_file():
    if platform.system() == "Windows":
        with open(f"{dir_path}/local.json", 'r') as config_file:
            return json.load(config_file)
    elif platform.system() == "Linux":
        with open(f"/var/www/haostool/config/linux_server.json", 'r') as config_file:
            return json.load(config_file)
    else:
        with open(f"/var/www/haostool/config/linux_server.json", 'r') as config_file:
            return json.load(config_file)
    
def get_database_uri():
    db_dict = get_config_file().get("database_info")
    address = db_dict.get("address")
    port = db_dict.get("port")
    user = db_dict.get("user")
    password = db_dict.get("password")
    database = db_dict.get("database")
    return f"mysql+pymysql://{user}:{password}@{address}:{port}/{database}?charset=utf8mb4"
    

class ConfigTypes(Enum):
    config = 1
    secrets = 2