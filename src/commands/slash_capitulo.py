import discord
from discord import app_commands
from discord.ext import commands

from src.services.biblia_cache import biblia_cache
from src.services.biblia_api import get_verses
from src.utils.helpers import split_text
from src.ui.paginator import Paginator

class SlashCapitulo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="capitulo",
        description="Obtém um capítulo da Bíblia"
    )
    @app_commands.describe(
        versao="Ex: nvi, ara, acf",
        livro="Ex: joao, genesis, romanos",
        capitulo="Número do capítulo",
    )
    async def capitulo(
        self,
        interaction: discord.Interaction,
        versao: str,
        livro: str,
        capitulo: int
    ):
        # 🔑 garante tempo para chamadas de API
        await interaction.response.defer()

        try:
            # 🔁 mesma lógica do comando prefixado
            versao_id = await biblia_cache.get_version_id(versao)
            livro_id = await biblia_cache.get_book_id(versao_id, livro)

            # Se 'versiculo' não foi passado, fazemos a requisição para o capítulo inteiro
            dados = await get_verses(
                version_id=versao_id,
                book_id=livro_id,
                chapter_id=capitulo
            )

            verses = dados.get("verses", [])
            if not verses:
                await interaction.followup.send(
                    "📭 Capítulo não encontrado."
                )
                return

            referencia = f"{livro.title()} {capitulo} ({versao.upper()})"
            texto_completo = "\n".join(
                f"**{v['verse_number']}** {v['text'].strip()}"
                for v in verses
            )
            
            pages = split_text(texto_completo)

            pages[0] = f"📖 **{referencia}**\n\n{pages[0]}"

            view = Paginator(pages=pages)

            await interaction.followup.send(
                content=pages[0],
                view=view
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Ocorreu um erro ao obter o Capítulo:\n```{e}```",
                ephemeral=True
            )


# 🔌 obrigatório para extensões
async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCapitulo(bot))
