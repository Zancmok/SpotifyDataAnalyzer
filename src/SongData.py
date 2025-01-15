"""
This module defines a data class for representing song-related data,
including its name, Spotify URI, play count, and playback duration.
"""

from dataclasses import dataclass


@dataclass
class SongData:
    """
    A data class representing information about a song.

    Attributes:
        name (str): The name of the song.
        spotify_uri (str): The Spotify URI of the song.
        times_played (int): The number of times the song has been played.
        ms_played (int): The total time (in milliseconds) the song has been played.
    """

    name: str
    spotify_uri: str
    times_played: int
    ms_played: int
    artist: str
