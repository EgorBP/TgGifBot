from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State


storage = MemoryStorage()


class FSMGifRegister(StatesGroup):
    """
    FSM для регистрации одной GIF.

    Состояния:
    - gif_id: хранение file_id GIF.
    - gif_tags: хранение тегов для GIF.
    """
    gif_id = State()
    gif_tags = State()


class FSMFindingGif(StatesGroup):
    """
    FSM для поиска GIF по тегам.

    Состояние:
    - find: ожидание ввода тегов пользователем.
    """
    find = State()


class FSMUpdatingTags(StatesGroup):
    """
    FSM для обновления тегов существующих GIF.

    Состояние:
    - updating: хранение данных о процессе обновления тегов.
    """
    updating = State()


class FSMGifSaving(StatesGroup):
    """
    FSM для процесса сохранения нескольких GIF.

    Состояния:
    - gifs_id: хранение списка file_id добавленных GIF.
    - gifs_tags: хранение тегов для этих GIF.
    """
    gifs_id = State()
    gifs_tags = State()
