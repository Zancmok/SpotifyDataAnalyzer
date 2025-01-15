"""
UserData.py

This module defines the UserData class, which represents a user's data in the context of Spotify play history.
"""

from dataclasses import dataclass
from SpotifyPlay import SpotifyPlay


@dataclass
class UserData:
    """
    Represents a user's data, including their identifier and play history.

    Attributes:
        user (str): The unique identifier or name of the user.
        play_history (list[SpotifyPlay]): A list of SpotifyPlay objects representing the user's playback history.
    """

    user: str
    play_history: list[SpotifyPlay]
