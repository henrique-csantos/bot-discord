from discord.ext import commands
from src.services.biblia_cache import biblia_cache
from src.services.biblia_api import search_exact_words

class BuscarCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="buscar")
    async def buscar(self, ctx, keyword: str, versao: str = "nvi"):
        try:
            version_id = await biblia_cache.get_version_id(versao)

            verses = await search_exact_words(
                version_id=version_id,
                keyword=keyword
            )

            if not verses:
                await ctx.send(f"Nenhum resultado encontrado para **{keyword}**.")
                return

            msg = f"📖 **Resultados para '{keyword}' ({versao.upper()})**\n\n"

            for i, v in enumerate(verses[:5], start=1):
                msg += (
                    f"{i}️⃣ {v['book_name']} "
                    f"{v['chapter']}:{v['verse_number']} — "
                    f"{v['text'].strip()}\n\n"
                )

            await ctx.send(msg[:2000])

        except Exception as e:
            await ctx.send(f"Ocorreu um erro na busca: {e}")

async def setup(bot):
    await bot.add_cog(BuscarCommand(bot))
