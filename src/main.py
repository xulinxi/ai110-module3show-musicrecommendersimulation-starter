"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

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

    for name, user_prefs in profiles.items():
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"  Genre: {user_prefs['genre']}, Mood: {user_prefs['mood']}, "
              f"Energy: {user_prefs['energy']}, Valence: {user_prefs['valence']}, "
              f"Danceability: {user_prefs['danceability']}, "
              f"Acoustic: {user_prefs['likes_acoustic']}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"    Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
