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
import time

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import base64
import secret
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
                name=content["master_metadata_track_name"] or content["episode_name"],
                artist=content["master_metadata_album_artist_name"] or "__unknown__"
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
                    ms_played=play.ms_played,
                    artist=play.artist
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


def generate_playlist(songs: list[SongData], playlist_id: str) -> None:
    """
    .
    """

    spotify: Spotify = Spotify(
        auth_manager=SpotifyOAuth(
            client_id=secret.CLIENT_ID,
            client_secret=secret.CLIENT_SECRET,
            redirect_uri="http://localhost:8888/callback",
            scope="playlist-modify-public playlist-modify-private"
        )
    )

    spotify.playlist_replace_items(
        playlist_id=playlist_id,
        items=[]
    )

    for i in range(0, len(songs), 100):
        while True:
            try:
                spotify.playlist_add_items(
                    playlist_id=playlist_id,
                    items=[song.spotify_uri for song in songs[i:i + 100]]
                )

                break
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after: int = 60

                    print(f"Rate limit hit. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    raise


def main() -> None:
    """

    :return:
    """

    data: list[UserData] = generate_data()

    USER_AMOUNT: int = 9
    SONGS_PER_USER: int = 50
    songs: list[SongData] = get_top_songs(data, song_amount=USER_AMOUNT * SONGS_PER_USER)

    """
    for i, song in enumerate(songs):
        print(f"{i + 1:4d} | {song.name:50s} | {song.artist:50s} | {song.ms_played:50d}")
    """

    generate_playlist(songs, secret.PLAYLIST_ID)


if __name__ == '__main__':
    main()
