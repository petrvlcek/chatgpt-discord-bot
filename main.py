from bot import ChatGPTBot
import os
import openai
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    openai.api_key = os.getenv('OPENAI_KEY')

    bot = ChatGPTBot()
    bot.run(token=discord_token)
