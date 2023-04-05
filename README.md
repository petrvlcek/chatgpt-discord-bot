# ChatGPT Discord Bot

ChatGPTBot is a Discord bot that uses OpenAI's GPT-3 to generate intelligent and realistic messages in chat channels.

## Running with Docker

* Build Docker image

```shell
 docker build -t petrvlcek/chatgpt-discord-bot:local . 
```

* Run Docker Compose
```shell
docker compose up -d
```

## Development

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

Copy `.env.template` file to `.env` and add your Discord bot token and your OpenAI API key.

```
DISCORD_BOT_TOKEN="your_token_here"
OPENAI_KEY="your_api_key_here"
```

* Run development server
```shell
uvicorn app.main:app --reload
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.