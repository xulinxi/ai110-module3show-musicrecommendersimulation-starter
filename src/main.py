"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, format_results_table, SCORING_MODES


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Sample user profiles representing different listener types
    profiles = {
        "Pop Enthusiast": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "valence": 0.82,
            "danceability": 0.80,
            "likes_acoustic": False,
        },
        "Chill Studier": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "valence": 0.58,
            "danceability": 0.55,
            "likes_acoustic": True,
        },
        "Workout Warrior": {
            "genre": "edm",
            "mood": "energetic",
            "energy": 0.93,
            "valence": 0.85,
            "danceability": 0.90,
            "likes_acoustic": False,
        },
        "Melancholic Folkster": {
            "genre": "folk",
            "mood": "melancholic",
            "energy": 0.30,
            "valence": 0.35,
            "danceability": 0.40,
            "likes_acoustic": True,
        },
    }

    # ── Default run: balanced mode with tabulate output (Challenge 4) ─
    print("\n" + "=" * 70)
    print("  SCORING MODE: balanced (default)")
    print("=" * 70)

    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(format_results_table(recommendations, name, user_prefs))

    # ── Challenge 2: Multiple Scoring Modes ───────────────────────────
    print("\n\n" + "#" * 70)
    print("  CHALLENGE 2: Comparing Scoring Modes for 'Pop Enthusiast'")
    print("#" * 70)

    pop_prefs = profiles["Pop Enthusiast"]
    for mode_name in ["genre-first", "mood-first", "energy-focused"]:
        print(f"\n--- Mode: {mode_name} ---")
        recs = recommend_songs(pop_prefs, songs, k=5, mode=mode_name)
        print(format_results_table(recs, f"Pop Enthusiast [{mode_name}]", pop_prefs))

    # ── Challenge 3: Diversity Penalty ────────────────────────────────
    print("\n\n" + "#" * 70)
    print("  CHALLENGE 3: Diversity Penalty (Chill Studier)")
    print("#" * 70)

    chill_prefs = profiles["Chill Studier"]

    print("\n--- WITHOUT diversity penalty ---")
    recs_no_div = recommend_songs(chill_prefs, songs, k=5)
    print(format_results_table(recs_no_div, "Chill Studier [no diversity]", chill_prefs))

    print("\n--- WITH diversity penalty ---")
    recs_div = recommend_songs(chill_prefs, songs, k=5, diversity=True)
    print(format_results_table(recs_div, "Chill Studier [diversity ON]", chill_prefs))

    # ── Challenge 1: Full-Feature Mode (new attributes) ───────────────
    print("\n\n" + "#" * 70)
    print("  CHALLENGE 1: Full-Feature Mode (5 new attributes)")
    print("#" * 70)

    full_feature_profile = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "danceability": 0.55,
        "likes_acoustic": True,
        # New Challenge 1 preferences
        "preferred_decade": "2020s",
        "preferred_mood_tags": ["nostalgic", "dreamy"],
        "target_instrumental": 0.85,
        "target_lyrics_sentiment": 0.10,
    }

    recs_full = recommend_songs(full_feature_profile, songs, k=5, mode="full-feature", diversity=True)
    print(format_results_table(recs_full, "Chill Studier [full-feature + diversity]", full_feature_profile))


if __name__ == "__main__":
    main()
