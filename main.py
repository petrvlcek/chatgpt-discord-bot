import asyncio

from fastapi import FastAPI

from app.bot import ChatGPTBot
from app.config import load_config
from app.healthchecks import HealthCheckService

app = FastAPI()
config = load_config()
bot = ChatGPTBot(config)
health = HealthCheckService(health_checks=[bot])


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.init())


@app.get("/health")
async def health_endpoint():
    return health.get_health()
