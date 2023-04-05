import os


class Configuration:

    def get_discord_token(self) -> str:
        pass

    def get_openai_api_key(self) -> str:
        pass


class EnvConfiguration(Configuration):
    def __init__(self):
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_KEY')

    def get_discord_token(self) -> str:
        return self.discord_token

    def get_openai_api_key(self) -> str:
        return self.openai_api_key
