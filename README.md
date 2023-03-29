# ChatGPT Discord Bot

ChatGPTBot is a Discord bot that uses OpenAI's GPT-3 to generate intelligent and realistic messages in chat channels.

## Installation

* Clone the repository.
* Create a virtual environment and activate it.

```shell
python3 -m venv env
source env/bin/activate
```

* Install the necessary dependencies.
```shell
pip install -r requirements.txt
```

Create a .env file in the project directory and add your Discord bot token and your OpenAI API key.

```
DISCORD_BOT_TOKEN="your_token_here"
OPENAI_KEY="your_api_key_here"
```


## Usage

Run the main.py script to start the Discord bot.

```
python main.py
```

The bot will now be active and listening for commands on Discord.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.