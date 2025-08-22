def prepare_tags_to_send(tags: list[str]):
    """
    Преобразовать список тегов в строку для отправки, добавляя символ '#' перед каждым тегом.

    Args:
        tags (list[str]): Список тегов.

    Returns:
        str: Строка с тегами в формате '#tag1, #tag2, ...'.
    """
    return f'#{", #".join(tags)}'


def execute_tags_from_message(message: str):
    """
    Извлечь теги из текста сообщения, удаляя символы '#' и приводя к нижнему регистру.

    Args:
        message (str): Текст сообщения с тегами (например, "#funny, #cat").

    Returns:
        list[str]: Список очищенных тегов в нижнем регистре.
    """
    gifs_tags: list[str] = message.replace('#', '').split(',')
    gifs_tags: list[str] = [f'{tag.strip().lower()}' for tag in gifs_tags]
    return gifs_tags
