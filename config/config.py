"""
This file contains all of the configuration values for the application.
"""
import json
import logging
import os
import platform
from enum import Enum
from app.exceptions.config import ConfigNotFoundException

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

def get_database_uri():
    if platform.system() == "Windows":
        db_dict = LOCAL_MYSQL_CONFIG
    else:
        print("Unknown system")
        return None
    address = db_dict.get("address")
    port = db_dict.get("port")
    user = db_dict.get("user")
    password = db_dict.get("password")
    database = db_dict.get("database")
    return f"mysql+pymysql://{user}:{password}@{address}:{port}/{database}"
    

class ConfigTypes(Enum):
    config = 1
    secrets = 2


__config_names = {
    ConfigTypes.config: 'config.json',
    ConfigTypes.secrets: 'secrets.json'
}


def get(name: ConfigTypes, folder='/afn/config/notifications'):
    """ Simple utility to fetch configs in /afn

    Args:
        name (ConfigTypes): The config type to retrieve
        folder (str): Can customize the location, but will search through the preset locations by default

    Returns:
        dict. A dictionary of the json object in the config

    Raises:
        IOError: If the config doesn't exist
    """
    config_file = __config_names.get(name)
    file_path = folder + os.sep + __config_names.get(name)

    if not os.path.isfile(file_path):
        __logger.error(
            'Found config directory ({folder}), but could not find the requested config file ({config})'.format(
                folder=folder, config=config_file
            )
        )
        raise ConfigNotFoundException(
            'Could not find the config in the specified location'
        )

    config_path = '{folder}/{name}'.format(name=config_file, folder=folder)

    with open(config_path, 'r') as fp:
        return json.load(fp)
