import asyncio

from fastapi import FastAPI

from bot import ChatGPTBot
from config import EnvConfiguration
from healthchecks import HealthCheckService

app = FastAPI()
config = EnvConfiguration()
bot = ChatGPTBot(config)
health = HealthCheckService(health_checks=[bot])


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.init())


@app.get("/health")
async def health_endpoint():
    return health.get_health()
