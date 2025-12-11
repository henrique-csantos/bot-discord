import discord
from src.services.bilbia_api import get_verses
from src.config import TOKEN

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')
        
        if message.content.startswith("!verso"):
            dados = get_verses(version_id=1, book_id=1, chapter_id=1, verse=1)
            texto = dados["verses"][0]["text"]

        await message.channel.send(texto)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)