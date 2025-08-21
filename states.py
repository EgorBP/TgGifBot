from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State


storage = MemoryStorage()


class FSMGifRegister(StatesGroup):
    gif_id = State()
    gif_tags = State()


class FSMFindingGif(StatesGroup):
    find = State()


class FSMUpdatingTags(StatesGroup):
    updating = State()


class FSMGifSaving(StatesGroup):
    gifs_id = State()
    gifs_tags = State()
