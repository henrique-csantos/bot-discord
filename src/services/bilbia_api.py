import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

BIBLIA_API_URL = os.getenv("BIBLIA_API_URL")
BIBLIA_API_KEY = os.getenv("BIBLIA_API_KEY")
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
CONTACT_INFO = os.getenv("CONTACT_INFO")

PROPRIETARY_USER_AGENT = f"{APP_NAME}/{APP_VERSION} ({CONTACT_INFO})"

headers = {
    "User-Agent": PROPRIETARY_USER_AGENT, 
    "Authorization": f"Bearer {BIBLIA_API_KEY}",
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def get_versions():
    """
    Função para a coleta das versões disponíveis na API da Bíblia.
    Retorna uma lista, mostrando as versões da biblia disponíveis e o id vinculado à elas.
    """
    response = requests.get(f"{BIBLIA_API_URL}get_versions.php", headers=headers)
    response.raise_for_status()
    return response.json()

def get_verses(version_id: int, book_id: int, chapter_id: int, verse: int = None, verse_start: int = None, verse_end: int = None):
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
    params = {
        "version_id": version_id,
        "book_id": book_id,
        "chapter_id": chapter_id,
        "verse": verse,
        "verse_start": verse_start,
        "verse_end": verse_end
    }

    response = requests.get(f"{BIBLIA_API_URL}get_verses.php", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

#obter versões disponíveis
# data = get_versions()

# for versao in data:
#     print(versao["id"], versao["name"])

#obter versículos
# verses_data = get_verses(version_id=1, book_id=1, chapter_id=1, verse=1)
# texto = verses_data["verses"][0]["text"]
# print(texto)
