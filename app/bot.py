import logging

import openai
import discord

from app.config import Configuration
from app.healthchecks import HealthCheck, HealthCheckStatus

_log = logging.getLogger(__name__)


class ChatGPTBot(discord.Client, HealthCheck):
    def __init__(self, config: Configuration, model: str = "gpt-3.5-turbo", role: str = "a nerd"):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.model = model
        self.role = role
        self.connected = False
        self.config = config

    async def init(self):
        openai.api_key = self.config.OPENAI_API_KEY
        discord.utils.setup_logging(
            handler=discord.utils.MISSING,
            formatter=discord.utils.MISSING,
            level=discord.utils.MISSING,
            root=False,
        )
        await self.start(self.config.DISCORD_BOT_TOKEN)

    def is_healthy(self) -> HealthCheckStatus:
        return HealthCheckStatus(self.__class__.__name__, is_healthy=self.connected)

    async def on_ready(self):
        self.connected = True
        _log.info('Logged on as', self.user)

    async def on_disconnect(self):
        self.connected = False
        _log.info('Disconnected form the server')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        if isinstance(message.channel, discord.Thread) and message.channel.owner == self.user:
            # reply in a thread owned by the bot
            async with message.channel.typing():
                messages = list()
                messages.append({"role": "system", "content": f"You are {self.role}"})
                async for msg in message.channel.history(limit=200, oldest_first=True):
                    role = "user"
                    if msg.author == self.user:
                        role = "assistant"
                    messages.append({"role": role, "content": msg.content})

                try:
                    response = await openai.ChatCompletion.acreate(
                        model=self.model,
                        messages=messages
                    )
                    answer = response.choices[0].message.content
                except openai.error.InvalidRequestError as e:
                    if e.code == "context_length_exceeded":
                        answer = "https://media.tenor.com/Lv-DF9iv7Q8AAAAC/christopher-walken-too-long-didnt-read.gif"
                    else:
                        answer = f"Something has failed: {e.user_message} (Error code: `{e.code}`)"
                except Exception as e:
                    answer = "Something has failed"

            await message.channel.send(content=answer)
        elif isinstance(message.channel, discord.TextChannel) and self.user in message.mentions:
            # create a new thread if the bot is mentioned in some channel
            async with message.channel.typing():
                # create a summary of the question and set it as a name of the thread
                summary_response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are {self.role}"},
                        {"role": "user", "content": "Get up to 4 words describing topic of this text: "
                                                    + message.content},
                    ]
                )
                question_summary = summary_response.choices[0].message.content
                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are {self.role}"},
                        {"role": "user", "content": message.content},
                    ]
                )
                answer = response.choices[0].message.content

            thread = await message.channel.create_thread(name=question_summary, type=discord.ChannelType.public_thread)
            await thread.send(content=answer)
