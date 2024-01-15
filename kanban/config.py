from pathlib import Path

import toml


def get_config():
    config = toml.load(open(Path('.config.toml').absolute()))
    return config['testing'] if config['TESTING'] else config['default']
