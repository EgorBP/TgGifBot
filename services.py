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

        file.seek(0)
        file.truncate(0)                    # Clear file

        data[user_id]['total_saved_gifs'] += 1

        new_gif_data = {
            f'gif_{data[user_id]['total_saved_gifs']}':
                {'gif_id': data_gif['gif_id'],
                 'gif_tags': data_gif['gif_tag']}
        }

        old_gif_data = data[user_id]['gifs_data']

        data[user_id]['gifs_data'] = old_gif_data | new_gif_data

        json.dump(data, file, indent=4, ensure_ascii=False)

        # print(data)
