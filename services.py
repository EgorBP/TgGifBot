import json
import os


def update_json(user_id: str, data_gif: dict) -> None:

    """We download json into the dict, change what we need in it, clear it
    old file and upload our modified file"""

    path = os.path.join('data', 'data.json')
    with open(path, 'r+') as file:
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
            {'gif_id': data_gif['gif_id'],
             'gif_tags': data_gif['gif_tag']}
    }

    old_gif_data = data[user_id]['gifs_data']
    data[user_id]['gifs_data'] = old_gif_data | new_gif_data

    with open(path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # print(data)


def load_gifs_data(user_id: str) -> dict | None:
    path = os.path.join('data', 'data.json')
    with open(path, 'r+') as file:
        try:
            data = json.load(file)
            gifs_data = data[user_id]['gifs_data']
            return gifs_data
        except (json.JSONDecodeError, KeyError):
            return None


def get_all_tags(user_id: str) -> str | None:
    all_gifs_data = load_gifs_data(user_id)
    if all_gifs_data is None:
        return None

    all_user_gif_tags = ', '.join([', '.join(one_gif_data['gif_tags']) for one_gif_data in all_gifs_data.values()])

    return all_user_gif_tags


def gif_finding():
    path = os.path.join('data', 'data.json')
    with open(path, 'r'):
        ...