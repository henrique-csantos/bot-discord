import discord
from discord.ext import commands
from src.config import TOKEN
from src.services.http_client import close_session

async def load_extensions(bot):
    await bot.load_extension("src.commands.versiculo")

async def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot conectado como {bot.user}")

    try:
        await load_extensions(bot)
        print("Comandos carregados:", bot.commands)
        await bot.start(TOKEN)
    finally:
        await close_session()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
