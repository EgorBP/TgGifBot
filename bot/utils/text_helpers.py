def prepare_tags_to_send(tags: list[str]):
    return f'#{", #".join(tags)}'


def execute_tags_from_message(message: str):
    gifs_tags: list[str] = message.replace('#', '').split(',')
    gifs_tags: list[str] = [f'{tag.strip().lower()}' for tag in gifs_tags]
    return gifs_tags
