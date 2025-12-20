import discord


class Paginator(discord.ui.View):
    """
    Uma interface de paginação para mensagens do Discord usando botões.
    Permite navegar entre várias páginas de conteúdo.
    :param pages: Lista de strings, cada uma representando uma página de conteúdo.
    :param timeout: Tempo em segundos antes da expiração da interface.
    """
    def __init__(
        self,
        pages: list[str],
        *,
        timeout: int = 120
    ):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.current_page = 0

    def _get_content(self):
        return self.pages[self.current_page]

    async def update(self, interaction: discord.Interaction):
        if interaction.response.is_done():
            await interaction.edit_original_response(
                content=self._get_content(),
                view=self
            )
        else:
            await interaction.response.edit_message(
                content=self._get_content(),
                view=self
            )


    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current_page > 0:
            self.current_page -= 1
        await self.update(interaction)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
        await self.update(interaction)
