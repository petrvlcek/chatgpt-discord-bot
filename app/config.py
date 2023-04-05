import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Configuration:
    DISCORD_BOT_TOKEN: str
    OPENAI_API_KEY: str


def load_config() -> Configuration:
    load_dotenv()
    return Configuration(
        DISCORD_BOT_TOKEN=required('DISCORD_BOT_TOKEN'),
        OPENAI_API_KEY=required('OPENAI_KEY')
    )


def required(key: str) -> str:
    if key in os.environ:
        return os.environ[key]
    else:
        raise RuntimeError(f"{key} environment variable is required")
