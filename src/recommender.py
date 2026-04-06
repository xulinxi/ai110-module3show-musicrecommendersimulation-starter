import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads a CSV file and returns a list of song dictionaries with numeric fields converted to int/float."""
    INT_FIELDS = {"id", "tempo_bpm"}
    FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in INT_FIELDS:
                row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (score, list of reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0
    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: up to +1.5
    energy_sim = 1.5 * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.2f})")

    # Valence similarity: up to +1.0
    valence_sim = 1.0 * (1 - abs(song["valence"] - user_prefs["valence"]))
    score += valence_sim
    reasons.append(f"valence similarity (+{valence_sim:.2f})")

    # Danceability similarity: up to +0.5
    dance_sim = 0.5 * (1 - abs(song["danceability"] - user_prefs["danceability"]))
    score += dance_sim
    reasons.append(f"danceability similarity (+{dance_sim:.2f})")

    # Acousticness bonus: +0.5 if user likes acoustic and song is acoustic
    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, sorts by score descending, and returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:k]
