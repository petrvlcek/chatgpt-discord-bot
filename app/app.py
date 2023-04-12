import asyncio

from quart import Quart
from bot import ChatGPTBot
from config import load_config
from healthchecks import HealthCheckService
from log_config import init_logging

app = Quart(__name__)

# set up logging
init_logging()

config = load_config()
bot = ChatGPTBot(config)
health = HealthCheckService(health_checks=[bot])


@app.before_serving
async def startup():
    asyncio.create_task(bot.init())


@app.route("/health")
async def health_endpoint():
    return vars(health.get_health()), 200

if __name__ == "__main__":
    app.run(debug=True)
