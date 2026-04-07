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
    likes_acoustic: bool
    target_valence: float = 0.5
    target_danceability: float = 0.5

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
    INT_FIELDS = {"id", "tempo_bpm", "popularity"}
    FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness", "instrumental", "lyrics_sentiment"}

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in INT_FIELDS:
                if key in row:
                    row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                if key in row:
                    row[key] = float(row[key])
            # Parse mood_tags from semicolon-separated string to list
            if "mood_tags" in row and isinstance(row["mood_tags"], str):
                row["mood_tags"] = [t.strip() for t in row["mood_tags"].split(";")]
            songs.append(row)
    return songs


# ══════════════════════════════════════════════════════════════════════
# Challenge 1: Advanced Song Features
# ══════════════════════════════════════════════════════════════════════
# New CSV columns added:
#   popularity       (0–100)  — how well-known the song is
#   release_decade   (string) — e.g. "2020s", "1990s"
#   mood_tags        (list)   — e.g. ["nostalgic", "dreamy"]
#   instrumental     (0.0–1.0) — how instrumental vs. vocal the track is
#   lyrics_sentiment (0.0–1.0) — positivity of lyrics (0 = no lyrics / dark, 1 = positive)


# ══════════════════════════════════════════════════════════════════════
# Challenge 2: Multiple Scoring Modes (Strategy Pattern)
# ══════════════════════════════════════════════════════════════════════
# Each strategy is a dict of weights. Users switch modes in main.py by name.

SCORING_MODES = {
    # Original baseline weights
    "balanced": {
        "genre": 2.0, "mood": 1.0, "energy": 1.5, "valence": 1.0,
        "dance": 0.5, "acoustic": 0.5,
        "popularity": 0.0, "decade": 0.0, "mood_tags": 0.0,
        "instrumental": 0.0, "lyrics_sentiment": 0.0,
    },
    # Genre is king — strongest genre pull, everything else secondary
    "genre-first": {
        "genre": 4.0, "mood": 0.5, "energy": 0.5, "valence": 0.5,
        "dance": 0.25, "acoustic": 0.25,
        "popularity": 0.0, "decade": 0.0, "mood_tags": 0.0,
        "instrumental": 0.0, "lyrics_sentiment": 0.0,
    },
    # Mood & emotion drive recommendations
    "mood-first": {
        "genre": 0.5, "mood": 3.0, "energy": 1.0, "valence": 1.5,
        "dance": 0.5, "acoustic": 0.5,
        "popularity": 0.0, "decade": 0.0, "mood_tags": 1.0,
        "instrumental": 0.0, "lyrics_sentiment": 0.5,
    },
    # Pure energy & danceability matching
    "energy-focused": {
        "genre": 0.5, "mood": 0.5, "energy": 3.0, "valence": 0.5,
        "dance": 1.5, "acoustic": 0.25,
        "popularity": 0.0, "decade": 0.0, "mood_tags": 0.0,
        "instrumental": 0.0, "lyrics_sentiment": 0.0,
    },
    # Uses all features including new Challenge 1 attributes
    "full-feature": {
        "genre": 1.5, "mood": 1.0, "energy": 1.5, "valence": 1.0,
        "dance": 0.5, "acoustic": 0.5,
        "popularity": 0.5, "decade": 0.5, "mood_tags": 0.75,
        "instrumental": 0.3, "lyrics_sentiment": 0.3,
    },
}

# ── Legacy weight configuration (kept for backwards compatibility) ────
# Choice 0 (Original):  GENRE=2.0, MOOD=1.0, ENERGY=1.5, VALENCE=1.0, DANCE=0.5, ACOUSTIC=0.5
# Choice 1 (Weight Shift): GENRE=1.0, MOOD=1.0, ENERGY=3.0, VALENCE=1.0, DANCE=0.5, ACOUSTIC=0.5
#   → halved genre (2.0→1.0), doubled energy (1.5→3.0)
# Choice 2 (Feature Removal): GENRE=2.0, MOOD=0.0, ENERGY=1.5, VALENCE=1.0, DANCE=0.5, ACOUSTIC=0.5
#   → mood check removed (1.0→0.0)
ACTIVE_CHOICE = 1  # Change to 0, 1, or 2 to switch experiments

WEIGHTS = {
    0: {"genre": 2.0, "mood": 1.0, "energy": 1.5, "valence": 1.0, "dance": 0.5, "acoustic": 0.5},
    1: {"genre": 1.0, "mood": 1.0, "energy": 3.0, "valence": 1.0, "dance": 0.5, "acoustic": 0.5},
    2: {"genre": 2.0, "mood": 0.0, "energy": 1.5, "valence": 1.0, "dance": 0.5, "acoustic": 0.5},
}

W = WEIGHTS[ACTIVE_CHOICE]


def score_song(user_prefs: Dict, song: Dict, mode: str = None) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (score, list of reasons).

    If mode is provided, uses the named strategy from SCORING_MODES.
    Otherwise falls back to the legacy ACTIVE_CHOICE weights (W).
    """
    if mode and mode in SCORING_MODES:
        w = SCORING_MODES[mode]
    else:
        # Legacy path: pad missing keys with 0.0 so new-feature code doesn't break
        w = {**{k: 0.0 for k in SCORING_MODES["balanced"]}, **W}

    score = 0.0
    reasons = []

    # Genre match
    if w["genre"] > 0 and song["genre"] == user_prefs["genre"]:
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    # Mood match
    if w["mood"] > 0 and song["mood"] == user_prefs["mood"]:
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    # Energy similarity
    energy_sim = w["energy"] * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.2f})")

    # Valence similarity
    valence_sim = w["valence"] * (1 - abs(song["valence"] - user_prefs["valence"]))
    score += valence_sim
    reasons.append(f"valence similarity (+{valence_sim:.2f})")

    # Danceability similarity
    dance_sim = w["dance"] * (1 - abs(song["danceability"] - user_prefs["danceability"]))
    score += dance_sim
    reasons.append(f"danceability similarity (+{dance_sim:.2f})")

    # Acousticness bonus
    if user_prefs["likes_acoustic"] and song.get("acousticness", 0) > 0.7:
        score += w["acoustic"]
        reasons.append(f"acoustic bonus (+{w['acoustic']:.1f})")

    # ── Challenge 1: Advanced feature scoring ────────────────────────

    # Popularity bonus: normalized 0-100 → 0.0-1.0, scaled by weight
    if w.get("popularity", 0) > 0 and "popularity" in song:
        pop_score = w["popularity"] * (song["popularity"] / 100.0)
        score += pop_score
        reasons.append(f"popularity bonus (+{pop_score:.2f})")

    # Decade preference: bonus if song matches user's preferred decade
    if w.get("decade", 0) > 0 and "preferred_decade" in user_prefs and "release_decade" in song:
        if song["release_decade"] == user_prefs["preferred_decade"]:
            score += w["decade"]
            reasons.append(f"decade match (+{w['decade']:.1f})")

    # Mood tags: partial credit for each overlapping tag
    if w.get("mood_tags", 0) > 0 and "preferred_mood_tags" in user_prefs and "mood_tags" in song:
        user_tags = set(user_prefs["preferred_mood_tags"])
        song_tags = set(song["mood_tags"]) if isinstance(song["mood_tags"], list) else set()
        overlap = len(user_tags & song_tags)
        total = max(len(user_tags), 1)
        tag_score = w["mood_tags"] * (overlap / total)
        if tag_score > 0:
            score += tag_score
            matching = ", ".join(user_tags & song_tags)
            reasons.append(f"mood tags [{matching}] (+{tag_score:.2f})")

    # Instrumental preference: similarity to user's target
    if w.get("instrumental", 0) > 0 and "target_instrumental" in user_prefs and "instrumental" in song:
        inst_sim = w["instrumental"] * (1 - abs(song["instrumental"] - user_prefs["target_instrumental"]))
        score += inst_sim
        reasons.append(f"instrumental similarity (+{inst_sim:.2f})")

    # Lyrics sentiment: similarity to user's target
    if w.get("lyrics_sentiment", 0) > 0 and "target_lyrics_sentiment" in user_prefs and "lyrics_sentiment" in song:
        sent_sim = w["lyrics_sentiment"] * (1 - abs(song["lyrics_sentiment"] - user_prefs["target_lyrics_sentiment"]))
        score += sent_sim
        reasons.append(f"lyrics sentiment (+{sent_sim:.2f})")

    return (score, reasons)


# ══════════════════════════════════════════════════════════════════════
# Challenge 3: Diversity Penalty
# ══════════════════════════════════════════════════════════════════════

def apply_diversity_penalty(
    scored: List[Tuple[Dict, float, str]],
    artist_penalty: float = 1.0,
    genre_penalty: float = 0.5,
) -> List[Tuple[Dict, float, str]]:
    """Re-ranks scored songs by penalizing repeated artists/genres in the top results.

    Walks through songs in score order. If a song's artist or genre already
    appeared in the selected list, its score is reduced before comparison.
    """
    selected = []
    seen_artists = {}   # artist → count
    seen_genres = {}    # genre → count

    for song, original_score, explanation in scored:
        penalty = 0.0
        penalty_reasons = []

        artist = song["artist"]
        genre = song["genre"]

        if artist in seen_artists:
            p = artist_penalty * seen_artists[artist]
            penalty += p
            penalty_reasons.append(f"repeat artist '{artist}' (-{p:.1f})")

        if genre in seen_genres:
            p = genre_penalty * seen_genres[genre]
            penalty += p
            penalty_reasons.append(f"repeat genre '{genre}' (-{p:.1f})")

        adjusted_score = original_score - penalty
        if penalty_reasons:
            explanation += "; " + "; ".join(penalty_reasons)

        selected.append((song, adjusted_score, explanation))
        seen_artists[artist] = seen_artists.get(artist, 0) + 1
        seen_genres[genre] = seen_genres.get(genre, 0) + 1

    # Re-sort after penalties
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = None,
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, optionally applies diversity penalty, and returns top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    if diversity:
        scored = apply_diversity_penalty(scored)

    return scored[:k]


# ══════════════════════════════════════════════════════════════════════
# Challenge 4: Visual Summary Table
# ══════════════════════════════════════════════════════════════════════

def format_results_table(
    recommendations: List[Tuple[Dict, float, str]],
    profile_name: str = "",
    user_prefs: Dict = None,
) -> str:
    """Formats recommendations as a readable table using the tabulate library."""
    from tabulate import tabulate

    lines = []

    # Header
    if profile_name:
        lines.append(f"\n{'='*70}")
        lines.append(f"  Profile: {profile_name}")
        if user_prefs:
            lines.append(
                f"  Genre: {user_prefs.get('genre', '?')}  |  "
                f"Mood: {user_prefs.get('mood', '?')}  |  "
                f"Energy: {user_prefs.get('energy', '?')}"
            )
        lines.append(f"{'='*70}")

    # Build table data
    table_data = []
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        reasons_formatted = "\n".join(f"  - {r}" for r in explanation.split("; "))
        table_data.append([
            rank,
            song["title"],
            song["artist"],
            f"{score:.2f}",
            reasons_formatted,
        ])

    lines.append(tabulate(
        table_data,
        headers=["#", "Song", "Artist", "Score", "Reasons"],
        tablefmt="fancy_grid",
        colalign=("center", "left", "left", "right", "left"),
    ))

    return "\n".join(lines)
