"""
main.py

This script processes Spotify user playback data to generate insights, such as the most-played songs.
It includes functionality to parse data from JSON files, filter by year, and compute aggregated statistics.

Functions:
    - generate_data: Loads and filters user playback data from JSON files in a specified directory.
    - get_top_songs: Computes the top songs based on playback duration from the loaded data.
    - main: Orchestrates the data generation and analysis process.
"""

import os
import json
from typing import Optional, Any
from SpotifyPlay import SpotifyPlay
from UserData import UserData
from SongData import SongData


def generate_data(data_directory_path: str = "..\\data", blacklist: Optional[list[str]] = None, years_allowed: Optional[list[str]] = None) -> list[UserData]:
    """
    Loads and processes user playback data from a specified directory.

    Args:
        data_directory_path (str): The path to the directory containing user data files. Defaults to "..\\data".
        blacklist (Optional[list[str]]): A list of user directories to exclude from processing. Defaults to None.
        years_allowed (Optional[list[str]]): A list of years to include in the playback data. Defaults to ["2024"].

    Returns:
        list[UserData]: A list of UserData objects representing each user's playback history.

    Raises:
        FileNotFoundError: If the specified directory does not exist or is not a directory.
    """

    if not years_allowed:
        years_allowed = ["2024"]

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
            if content["ts"][:4] not in years_allowed:
                continue

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
                offline=content["offline"],
                name=content["master_metadata_track_name"] or content["episode_name"]
            ))

        out.append(UserData(
            user=path,
            play_history=formated_contents
        ))

    return out


def get_top_songs(data: list[UserData], song_amount: int = 100) -> list[SongData]:
    """
    Computes the top songs by playback duration from a list of user data.

    Args:
        data (list[UserData]): The list of user playback histories to analyze.
        song_amount (int): The maximum number of top songs to return. Defaults to 100.

    Returns:
        list[SongData]: A list of SongData objects representing the top songs sorted by playback duration.
    """

    songs: dict[str, SongData] = {}

    for user in data:
        for play in user.play_history:
            if play.uri not in songs:
                songs[play.uri] = SongData(
                    name=play.name,
                    spotify_uri=play.uri,
                    times_played=1,
                    ms_played=play.ms_played
                )
            else:
                songs[play.uri].times_played += 1
                songs[play.uri].ms_played += play.ms_played

    out: list[SongData] = [songs[song] for song in songs]

    out.sort(
        key=lambda x: x.ms_played,
        reverse=True
    )

    return out[:song_amount]


def main() -> None:
    """

    :return:
    """

    data: list[UserData] = generate_data()

    songs: list[SongData] = get_top_songs(data, song_amount=800)

    for i, song in enumerate(songs):
        print(f"{i + 1:4d} | {song.name:50s} | {song.ms_played:50d}")


if __name__ == '__main__':
    main()
