from src.services.http_client import get_session, BIBLIA_API_URL

async def get_versions():
    """
    Função para a coleta das versões disponíveis na API da Bíblia.
    Retorna uma lista, mostrando as versões da biblia disponíveis e o id vinculado à elas.
    """
    url = f"{BIBLIA_API_URL}get_versions.php"
    async with get_session() as session:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            print("[DEBUG] URL:", response.url)
            return await response.json()

async def get_verses(version_id: int, book_id: int, chapter_id: int, verse: int = None, verse_start: int = None, verse_end: int = None):
    """
    Função para a coleta dos versículos de uma determinada versão, livro, capítulo e versículo(s).
    
    :param version_id: ID da versão da Bíblia
    :type version_id: int
    :param book_id: ID do livro da Bíblia
    :type book_id: int
    :param chapter_id: Número do capítulo
    :type chapter_id: int
    :param verse: Número do versículo específico
    :type verse: int
    :param verse_start: Número do versículo inicial para um intervalo
    :type verse_start: int
    :param verse_end: Número do versículo final para um intervalo
    :type verse_end: int
    """
    url = f"{BIBLIA_API_URL}get_verses.php"
    params = {
        "version_id": version_id,
        "book_id": book_id,
        "chapter_id": chapter_id,
    }
    
    print("[DEBUG] GET get_verses.php")
    print("[DEBUG] Params:", params)

    # Apenas adiciona o parâmetro se ele existir
    if verse is not None:
        params["verse"] = verse
    if verse_start is not None:
        params["verse_start"] = verse_start
    if verse_end is not None:
        params["verse_end"] = verse_end


    async with get_session() as session:
        async with session.get(url, params=params, timeout=10) as response:
            response.raise_for_status()
            print("[DEBUG] URL:", response.url)
            return await response.json()

#obter versões disponíveis
# data = get_versions()

# for versao in data:
#     print(versao["id"], versao["name"])

#obter versículos
# verses_data = get_verses(version_id=1, book_id=1, chapter_id=1, verse=1)
# texto = verses_data["verses"][0]["text"]
# print(texto)
