import aiohttp
import unicodedata

URL_VERSIONS = "https://pesquisarnabiblia.com.br/api-projeto/api/get_versions.php"
URL_BOOKS = "https://pesquisarnabiblia.com.br/api-projeto/api/get_books.php"

class BibliaCache:

    def __init__(self):
        self._versions = None        # { normalized_name: id }
        self._books = {}             # { version_id: { normalized_book: id } }

    # ------------------------------
    # Utils
    # ------------------------------
    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = unicodedata.normalize("NFKD", text)
        return "".join(ch for ch in text if not unicodedata.combining(ch))

    # ------------------------------
    # Carrega versões
    # ------------------------------
    async def load_versions(self):
        if self._versions is not None:
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(URL_VERSIONS) as resp:
                data = await resp.json()

        self._versions = {}
        for item in data:
            normalized = self.normalize(item["abbrev"])
            self._versions[normalized] = int(item["id"])

    # ------------------------------
    # Carrega livros de uma versão
    # ------------------------------
    async def load_books(self, version_id: int):
        if version_id in self._books:
            return

        params = {"version_id": version_id}

        async with aiohttp.ClientSession() as session:
            async with session.get(URL_BOOKS, params=params) as resp:
                data = await resp.json()

        books_map = {}

        for item in data:
            # abreviações
            normalized_abbrev = self.normalize(item["abbrev"])
            books_map[normalized_abbrev] = int(item["id"])

            # nome completo
            normalized_name = self.normalize(item["name"])
            books_map[normalized_name] = int(item["id"])

        self._books[version_id] = books_map

    # ------------------------------
    # GETTERS REALMENTE USADOS PELO BOT
    # ------------------------------
    async def get_version_id(self, version_name: str) -> int:
        """Retorna o ID da versão baseado na sigla. (ex: 'nvi')"""
        await self.load_versions()

        norm = self.normalize(version_name)

        if norm not in self._versions:
            raise ValueError(f"Versão desconhecida: {version_name}")

        return self._versions[norm]

    async def get_book_id(self, version_id: int, book_name: str) -> int:
        """Retorna o ID do livro baseado na abreviação OU nome completo."""
        await self.load_books(version_id)

        norm = self.normalize(book_name)

        if norm not in self._books[version_id]:
            raise ValueError(f"Livro desconhecido: {book_name}")

        return self._books[version_id][norm]


# Instância única usada pelo bot
biblia_cache = BibliaCache()
