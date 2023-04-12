from logging.config import dictConfig

import yaml


def init_logging():
    with open('log_config.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
        dictConfig(config)

