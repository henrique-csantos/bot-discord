import discord
from discord import app_commands
from discord.ext import commands

from src.services.biblia_cache import biblia_cache
from src.services.biblia_api import search_exact_words
from src.utils.helpers import split_text
from src.ui.paginator import Paginator


class SlashBuscar(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="buscar",
        description="Busca uma palavra na Bíblia inteira ou em uma versão específica"
    )
    @app_commands.describe(
        keyword="Palavra exata a ser buscada",
        versao="Ex: nvi, ara, acf (opcional)"
    )
    async def buscar(
        self,
        interaction: discord.Interaction,
        keyword: str,
        versao: str = "nvi"
    ):
        # ⏳ garante tempo para chamadas longas
        await interaction.response.defer()

        try:
            # 🔁 resolve versão
            versao_id = await biblia_cache.get_version_id(versao)

            # 🔍 chamada da API
            verses = await search_exact_words(
                version_id=versao_id,
                keyword=keyword
            )

            if not verses:
                await interaction.followup.send(
                    f"📭 Nenhum resultado encontrado para **{keyword}**.",
                    ephemeral=True
                )
                return

            # 🧱 monta texto completo
            texto_completo = "\n\n".join(
                f"**{v['book_name']} {v['chapter']}:{v['verse_number']}**\n{v['text'].strip()}"
                for v in verses
            )

            # ✂️ quebra em páginas
            pages = split_text(texto_completo)

            header = f"📖 **Resultados para '{keyword}' ({versao.upper()})**\n\n"
            pages[0] = header + pages[0]

            view = Paginator(pages=pages)

            await interaction.followup.send(
                content=pages[0],
                view=view
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Ocorreu um erro na busca:\n```{e}```",
                ephemeral=True
            )


# 🔌 obrigatório para extensões
async def setup(bot: commands.Bot):
    await bot.add_cog(SlashBuscar(bot))
