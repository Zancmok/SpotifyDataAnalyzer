"""
main.py
"""

import os
import json
from typing import Optional, Any
from SpotifyPlay import SpotifyPlay
from UserData import UserData


def generate_data(data_directory_path: str = "..\\data", blacklist: Optional[list[str]] = None) -> list[UserData]:
    """

    :return:
    """

    out: list[UserData] = []

    if not os.path.exists(data_directory_path):
        raise FileNotFoundError(f"Directory not found: '{data_directory_path}'")

    if not os.path.isdir(data_directory_path):
        raise FileNotFoundError(f"Path doesn't lead to a directory: '{data_directory_path}'")

    for path in os.listdir(data_directory_path):
        if not os.path.exists(os.path.join(data_directory_path, path)):
            continue

        if blacklist and path in blacklist:
            continue

        contents: list[dict[str, Any]] = []

        for file in os.listdir(os.path.join(data_directory_path, path)):
            if file[::-1][:4][::-1] != "json":
                continue

            with open(os.path.join(data_directory_path, path, file), 'r', encoding="utf-8") as file_object:
                contents += json.load(file_object)

        formated_contents: list[SpotifyPlay] = []

        for content in contents:
            formated_contents.append(SpotifyPlay(
                timestamp=content["ts"],
                platform=content["platform"],
                ms_played=content["ms_played"],
                country=content["conn_country"],
                uri=content["spotify_track_uri"] or content["spotify_episode_uri"],
                reason_start=content["reason_start"],
                reason_end=content["reason_end"],
                shuffle=content["shuffle"],
                skipped=content["skipped"],
                offline=content["offline"]
            ))

        out.append(UserData(
            user=path,
            play_history=formated_contents
        ))

    return out


def main() -> None:
    """

    :return:
    """

    data: list[UserData] = generate_data()

    print(data)


if __name__ == '__main__':
    main()
