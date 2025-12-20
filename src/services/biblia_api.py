from src.services.http_client import get_session, fetch_with_retry, BIBLIA_API_URL

async def get_versions():
    """
    Função para a coleta das versões disponíveis na API da Bíblia.
    Retorna uma lista, mostrando as versões da biblia disponíveis e o id vinculado à elas.
    """
    url = f"{BIBLIA_API_URL}get_versions.php"
    session = get_session()
    data = await fetch_with_retry(session, "GET", url)
    return data

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


    session = get_session()
    data = await fetch_with_retry(session, "GET", url, params=params)
    return data
        
async def search_exact_words(
    version_id: int,
    keyword: str,
    book_id: int | None = None,
    chapter_id: int | None = None,
    verse_start: int | None = None,
    verse_end: int | None = None,
):
    """
    Função para buscar versículos que contenham exatamente uma palavra-chave específica.
    :param version_id: ID da versão da Bíblia
    :param keyword: Palavra-chave a ser buscada
    :param book_id: ID do livro da Bíblia (opcional)
    :param chapter_id: Número do capítulo (opcional)
    :param verse_start: Número do versículo inicial para um intervalo (opcional)
    :param verse_end: Número do versículo final para um intervalo (opcional)
    """
    url = f"{BIBLIA_API_URL}search_exact_words.php"

    params = {
        "version_id": version_id,
        "keyword": keyword
    }

    if book_id is not None:
        params["book_id"] = book_id

    if chapter_id is not None:
        params["chapter_id"] = chapter_id

    if verse_start is not None and verse_end is not None:
        if verse_start > verse_end:
            raise ValueError("verse_start não pode ser maior que verse_end")
        params["verse_start"] = verse_start
        params["verse_end"] = verse_end

    print("[DEBUG] search_exact_words params:", params)

    session = get_session()
    data = await fetch_with_retry(
        session,
        "GET",
        f"{BIBLIA_API_URL}/search_exact_words.php",
        params={
            "version_id": version_id,
            "keyword": keyword
        }
    )

    # ✅ garante contrato estável
    return data.get("verses", [])