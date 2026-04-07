"""
Adversarial / edge-case user profiles to stress-test the scoring logic.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    adversarial_profiles = {
        # 1. Conflicting: high energy but sad mood
        #    Energy 0.9 should favor intense/EDM tracks, but mood "melancholic"
        #    only matches folk song (energy 0.31). Which signal wins?
        "High-Energy Sad Person": {
            "genre": "folk",
            "mood": "melancholic",
            "energy": 0.95,
            "valence": 0.20,
            "danceability": 0.30,
            "likes_acoustic": False,
        },

        # 2. Non-existent genre — genre bonus (+2.0) never fires.
        #    Can numeric features alone produce sensible results?
        "Ghost Genre (reggaeton)": {
            "genre": "reggaeton",
            "mood": "happy",
            "energy": 0.80,
            "valence": 0.80,
            "danceability": 0.85,
            "likes_acoustic": False,
        },

        # 3. All numeric features at 0.0 — extreme floor
        #    Expects the quietest, saddest, least danceable songs.
        "All-Zeros Minimalist": {
            "genre": "ambient",
            "mood": "somber",
            "energy": 0.0,
            "valence": 0.0,
            "danceability": 0.0,
            "likes_acoustic": True,
        },

        # 4. All numeric features at 1.0 — extreme ceiling
        #    No song has perfect 1.0 across the board, so who gets closest?
        "All-Ones Maximalist": {
            "genre": "electronic",
            "mood": "euphoric",
            "energy": 1.0,
            "valence": 1.0,
            "danceability": 1.0,
            "likes_acoustic": False,
        },

        # 5. Acoustic EDM — contradictory preferences.
        #    EDM songs have ~0.03-0.04 acousticness, so genre match
        #    fires but acoustic bonus never does. Meanwhile acoustic songs
        #    get the +0.5 bonus but no genre match (+2.0). Who wins?
        "Acoustic EDM Fan": {
            "genre": "edm",
            "mood": "uplifting",
            "energy": 0.90,
            "valence": 0.85,
            "danceability": 0.90,
            "likes_acoustic": True,
        },

        # 6. Perfectly average — all features at 0.5.
        #    Tests whether the system has a "bland middle" bias.
        "Mr. Average (all 0.5)": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.50,
            "valence": 0.50,
            "danceability": 0.50,
            "likes_acoustic": False,
        },

        # 7. Wants chill but hates acoustic — lofi/ambient songs are
        #    highly acoustic, so likes_acoustic=False means no bonus.
        #    But there's no penalty either, so acoustic songs still rank
        #    high. Exposes asymmetric acoustic scoring.
        "Anti-Acoustic Chiller": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.60,
            "danceability": 0.55,
            "likes_acoustic": False,
        },

        # 8. Genre says pop, but all numeric features match metal.
        #    Pop genre bonus (+2.0) vs. metal's perfect numeric alignment.
        #    Can numeric similarity ever overcome a genre mismatch?
        "Pop Fan with Metal Tastes": {
            "genre": "pop",
            "mood": "aggressive",
            "energy": 0.97,
            "valence": 0.22,
            "danceability": 0.55,
            "likes_acoustic": False,
        },
    }

    for name, user_prefs in adversarial_profiles.items():
        print(f"\n{'='*62}")
        print(f"  ADVERSARIAL PROFILE: {name}")
        print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  "
              f"Energy: {user_prefs['energy']}")
        print(f"  Valence: {user_prefs['valence']}  |  Dance: {user_prefs['danceability']}"
              f"  |  Acoustic: {'Yes' if user_prefs['likes_acoustic'] else 'No'}")
        print(f"{'='*62}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n  {'#':<4} {'Song':<28} {'Artist':<20} {'Score':>5}")
        print(f"  {'-'*4} {'-'*28} {'-'*20} {'-'*5}")

        for rank, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"  {rank:<4} {song['title']:<28} {song['artist']:<20} {score:>5.2f}")
            for reason in explanation.split("; "):
                print(f"         - {reason}")
            print()


if __name__ == "__main__":
    main()
