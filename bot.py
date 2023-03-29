import openai
from discord import ChannelType
import discord


class ChatGPTBot(discord.Client):
    def __init__(self, model="gpt-3.5-turbo", role="a nerd"):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.model = model
        self.role = role

    async def on_ready(self):
        print('Logged on as', self.user)

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

                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=messages
                )
                answer = response.choices[0].message.content
            await message.channel.send(content=answer)
        elif isinstance(message.channel, discord.TextChannel) and self.user in message.mentions:
            # create a new thread if the bot is mentioned in some channel
            async with message.channel.typing():
                # create a summary of the question and set it as a name of the thread
                summary_response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are {self.role}"},
                        {"role": "user", "content": "Summarize this text in max 4 words "
                                                    "without any interpunction at the end: "
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

            thread = await message.channel.create_thread(name=question_summary, type=ChannelType.public_thread)
            await thread.send(content=answer)
