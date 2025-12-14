import unicodedata
from src.services.http_client import get_session

URL_VERSIONS = "https://pesquisarnabiblia.com.br/api-projeto/api/get_versions.php"
URL_BOOKS = "https://pesquisarnabiblia.com.br/api-projeto/api/get_books.php"

VERSION_ALIASES = {
    "nvi": "nova versao internacional",
    "acf": "almeida corrigida e fiel",
    "ara": "almeida revista e atualizada",
    "arc": "almeida revista e corrigida",
    "kjv": "king james version",
    "kja": "king james atualizada",
    "tb": "traducao brasileira"
}


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

        async with get_session() as session:
            async with session.get(URL_VERSIONS) as resp:
                data = await resp.json()
                print("[DEBUG] Loaded versions:", data)

        self._versions = {}

        for item in data:
            name_norm = self.normalize(item["name"])
            self._versions[name_norm] = int(item["id"])


    # ------------------------------
    # Carrega livros de uma versão
    # ------------------------------
    async def load_books(self, version_id: int):
        if version_id in self._books:
            return

        params = {"version_id": version_id}

        async with get_session() as session:
            async with session.get(URL_BOOKS, params=params) as resp:
                data = await resp.json()

        books_map = {}

        for item in data:
            name = self.normalize(item["name"])
            books_map[name] = int(item["id"])

        self._books[version_id] = books_map


    # ------------------------------
    # GETTERS USADOS PELO BOT
    # ------------------------------
    async def get_version_id(self, version_input: str) -> int:
        await self.load_versions()

        norm = self.normalize(version_input)

        # resolver alias (nvi → nova versao internacional)
        norm = VERSION_ALIASES.get(norm, norm)

        if norm not in self._versions:
            raise ValueError(f"Versão desconhecida: {version_input}")

        return self._versions[norm]


    async def get_book_id(self, version_id: int, book_name: str) -> int:
        await self.load_books(version_id)

        norm = self.normalize(book_name)

        if norm not in self._books[version_id]:
            raise ValueError(f"Livro desconhecido: {book_name}")

        return self._books[version_id][norm]


biblia_cache = BibliaCache()
