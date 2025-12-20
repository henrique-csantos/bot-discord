import discord
from discord.ext import commands
from src.config import TOKEN

GUILD_ID = 954612798715985940


async def load_extensions(bot: commands.Bot):
    await bot.load_extension("src.commands.versiculo")
    await bot.load_extension("src.commands.buscar")
    await bot.load_extension("src.commands.slash_versiculo")
    await bot.load_extension("src.commands.slash_capitulo")
    await bot.load_extension("src.commands.slash_buscar")


async def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    # 🔹 EVENTOS DEVEM SER DEFINIDOS ANTES DE STARTAR O BOT
    @bot.event
    async def on_ready():
        guild = discord.Object(id=GUILD_ID)
        print(f"Bot conectado como {bot.user}")

        # Copia comandos globais para o servidor de teste
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)


        for cmd in bot.tree.get_commands():
            print("Slash:", cmd.name)

        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"Slash commands sincronizados: {len(synced)}")
        except Exception as e:
            print("Erro ao sincronizar slash commands:", e)

    @bot.event
    async def on_close():
        print("Encerrando bot e fechando sessão HTTP...")
        # await close_session()

    # 🔹 lifecycle correto
    async with bot:
        await load_extensions(bot)
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
