import discord
from discord import app_commands
from discord.ext import commands

from src.services.biblia_cache import biblia_cache
from src.services.biblia_api import get_verses

class SlashVersiculo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="versiculo",
        description="Obtém um versículo da Bíblia"
    )
    @app_commands.describe(
        versao="Ex: nvi, ara, acf",
        livro="Ex: joao, genesis, romanos",
        capitulo="Número do capítulo",
        versiculo="(Opcional) Número do versículo"
    )
    async def versiculo(
        self,
        interaction: discord.Interaction,
        versao: str,
        livro: str,
        capitulo: int,
        versiculo: int  # Isso já garante que 'versiculo' é opcional
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
                chapter_id=capitulo,
                verse=versiculo  # 'versiculo' pode ser None, o que fará a API retornar todos os versículos do capítulo
            )

            verses = dados.get("verses", [])
            if not verses:
                await interaction.followup.send(
                    "📭 Versículo não encontrado."
                )
                return

            # Se 'versiculo' foi passado, mostramos o versículo específico
            if versiculo is not None:
                versiculo = int(versiculo)
                texto = verses[0]["text"].strip()
                referencia = f"{livro.title()} {capitulo}:{versiculo} ({versao.upper()})"
                await interaction.followup.send(
                    f"📖 **{referencia}**\n{texto}"
                )
            # Caso contrário, mostramos todos os versículos do capítulo
            else:
                referencia = f"{livro.title()} {capitulo} ({versao.upper()})"
                texto = "\n".join(
                    f"**{v['verse_number']}** {v['text'].strip()}"
                    for v in verses
                )

                await interaction.followup.send(
                    f"📖 **{referencia}**\n{texto[:1900]}"  # Limitando o texto a 1900 caracteres
                )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Ocorreu um erro ao obter o versículo:\n```{e}```",
                ephemeral=True
            )


# 🔌 obrigatório para extensões
async def setup(bot: commands.Bot):
    await bot.add_cog(SlashVersiculo(bot))
