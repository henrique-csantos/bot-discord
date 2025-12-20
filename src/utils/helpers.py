def split_text(text: str, limit: int = 1900) -> list[str]:
    """
    Divide um texto em várias partes, cada uma com um tamanho máximo especificado.
    :param text: O texto a ser dividido
    :param limit: O tamanho máximo de cada parte
    :return: Uma lista de partes do texto
    """
    pages = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            pages.append(current)
            current = line
        else:
            current += "\n" + line if current else line

    if current:
        pages.append(current)

    return pages
