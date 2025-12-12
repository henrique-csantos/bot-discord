import discord
from discord.ext import commands
from src.config import TOKEN

async def load_extensions(bot):
    await bot.load_extension("src.commands.versiculo")

async def main():

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot conectado como {bot.user}")

    # CHAMADA CORRETA — passando o bot
    await load_extensions(bot)

    # Confirmar que o comando foi registrado
    print("Comandos carregados:", bot.commands)

    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
