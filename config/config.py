import json
import logging
import os
from enum import Enum
from app.exceptions.config import ConfigNotFoundException

__logger = logging.getLogger(__file__)


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
