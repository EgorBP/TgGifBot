import json
import os

from aiogram.types import Message


def update_json_by_new_gif(user_id: str, gif_data: dict) -> None:

    """We download json into the dict, change what we need in it, clear it
    old file and upload our modified file"""

    path = os.path.join('data', 'data.json')
    with open(path, 'r') as file:
        try:                                # Try to open json, if empty
            data = json.load(file)          # set new data
            try:
                data[user_id]
            except KeyError:
                data[user_id] = {
                'total_saved_gifs': 0,
                'gifs_data': {}
                }
        except json.JSONDecodeError:
            data = {user_id: {
                'total_saved_gifs': 0,
                'gifs_data': {}
            }}
        # print(data)

    data[user_id]['total_saved_gifs'] += 1

    new_gif_data = {
        f'gif_{data[user_id]['total_saved_gifs']}':
            {'gif_id': gif_data['gif_id'],
             'gif_tags': gif_data['gif_tag']}
    }

    old_gif_data = data[user_id]['gifs_data']
    data[user_id]['gifs_data'] = old_gif_data | new_gif_data

    with open(path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # print(data)


def update_json_by_deleting_gif(new_data: dict):
    path = os.path.join('data', 'data.json')
    with open(path, 'w') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)


def load_all_data(message: Message) -> dict | None:
    user_id = str(message.from_user.id)
    path = os.path.join('data', 'data.json')
    with open(path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except (json.JSONDecodeError, KeyError):
            return None



def load_gifs_data(message: Message) -> dict | None:
    user_id = str(message.from_user.id)
    all_data = load_all_data(message)
    if all_data is None or all_data == {}:
        return None

    gifs_data = all_data[user_id]['gifs_data']
    return gifs_data


def get_all_tags(message: Message) -> str | None:
    all_gifs_data = load_gifs_data(message)
    if all_gifs_data is None:
        return None

    all_user_gif_tags = ', '.join([', '.join(one_gif_data['gif_tags']) for one_gif_data in all_gifs_data.values()])

    return all_user_gif_tags


def get_all_tags_separated(message: Message) -> str | None:
    all_gifs_data = load_gifs_data(message)
    if all_gifs_data is None:
        return None

    all_user_gif_tags = '; '.join([', '.join(one_gif_data['gif_tags']) for one_gif_data in all_gifs_data.values()])

    return all_user_gif_tags


def gif_finding(message: Message):
    all_gifs_data = load_gifs_data(message)
    if all_gifs_data is None:
        return None

