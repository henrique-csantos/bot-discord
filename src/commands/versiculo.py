from discord.ext import commands
from src.services.biblia_cache import biblia_cache
from src.services.biblia_api import get_verses

class VersiculoCommand(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="versiculo", help="Obtém um versículo: !versiculo <version_id> <book_id> <chapter> <verse>")
    async def versiculo_formatado(self, ctx, versao: str, livro: str, cap: int, vers: int):
        """
        Comando para obter um versículo específico da Bíblia.
        
        :param ctx: Contexto do comando
        :param versao: ID da versão da Bíblia
        :param livro: ID do livro da Bíblia
        :param cap: Número do capítulo
        :param vers: Número do versículo
        """
        try:
            versao_id = await biblia_cache.get_version_id(versao)
            livro_id = await biblia_cache.get_book_id(versao_id, livro)

            dados = await get_verses(
                version_id=versao_id,
                book_id=livro_id,
                chapter_id=cap,
                verse=vers
            )
            verses = dados.get("verses", [])
            if not verses:
                await ctx.send("Versículo não encontrado.")
                return
            
            texto = verses[0].get("text", "").strip()
            referencia = f"Versão {versao}, Livro {livro}, Capítulo {cap}, Versículo {vers}"
            await ctx.send(f"📖 **{referencia}**\n{texto}")
        
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao obter o versículo: {e}")

async def setup(bot):
    await bot.add_cog(VersiculoCommand(bot))