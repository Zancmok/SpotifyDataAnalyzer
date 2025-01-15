"""
SpotifyPlay.py

This module defines the SpotifyPlay data class, which represents a single instance of a Spotify play event.
"""

from dataclasses import dataclass


@dataclass
class SpotifyPlay:
    """
    Represents a Spotify play event, including metadata about the play.

    Attributes:
        timestamp (str): The timestamp of when the play occurred.
        platform (str): The platform used to play the track (e.g., "Android OS", "Google Chromecast").
        ms_played (int): The duration of the play in milliseconds.
        country (str): The country code of where the play occurred.
        uri (str): The Spotify URI of the track.
        reason_start (str): The reason the play started (e.g., "trackdone").
        reason_end (str): The reason the play ended (e.g., "endplay").
        shuffle (bool): Whether shuffle mode was enabled during the play.
        skipped (bool): Whether the track was skipped.
        offline (bool): Whether the play occurred in offline mode.
    """

    timestamp: str
    platform: str
    ms_played: int
    country: str
    uri: str
    reason_start: str
    reason_end: str
    shuffle: bool
    skipped: bool
    offline: bool
    name: str
    artist: str
