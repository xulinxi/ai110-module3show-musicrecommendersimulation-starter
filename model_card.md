# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodSync 1.0**

---

## 2. Intended Use  

This recommender suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy level, valence, danceability, and acoustic preference. It is designed for classroom exploration only, not for real users or production deployment. It assumes the user has a single fixed taste profile for the entire session and that preferences can be captured by a handful of numeric values.

**Not intended for:** real music streaming, commercial use, or any context where users expect diverse, evolving recommendations across large catalogs.

---

## 3. How the Model Works  

The recommender gives every song in the catalog a score based on how closely it matches what the user asked for, then returns the top 5 highest-scoring songs.

It checks six things. First, does the song's genre match the user's favorite genre? That's the biggest factor — worth up to 2 points. Second, does the mood match? That adds 1 point. Then it looks at three numeric features — energy, valence (how happy or sad the song sounds), and danceability — and measures how close each one is to the user's target. The closer the match, the more points the song earns. Finally, if the user said they like acoustic music and the song has high acousticness, it gets a small bonus.

All six factors add up to a maximum of about 6.5 points. The system scores every song, sorts them from highest to lowest, and picks the top 5. Each recommendation comes with an explanation showing exactly which factors contributed to its score.

We also built a configurable weight system (Choice 0, 1, 2) so we could experiment with different balances — for example, making energy twice as important while cutting genre's influence in half.

---

## 4. Data  

The catalog contains **20 songs** in `data/songs.csv`, spanning 17 genres and 16 moods. Each song has 10 attributes: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

The starter dataset originally contained **10 songs** (id 1–10, covering pop, lofi, rock, ambient, jazz, synthwave, and indie pop). We added **10 more songs** (id 11–20) to increase genre and mood diversity — introducing hip hop, folk, electronic, blues, metal, r&b, latin, classical, edm, and country. Despite the expansion, the data still has notable imbalances: 15 of 17 genres have only one song each (only lofi has 3 and pop has 2). The catalog skews high-energy (10 songs above 0.7, only 4 in the mid-range) and high-valence (9 songs above 0.7, only 3 below 0.4). Tempo ranges from 56 to 168 BPM but is not used in scoring. Missing from the dataset: languages other than English, podcast-style content, live recordings, and many mainstream genres like R&B sub-genres, K-pop, or reggae.

---

## 5. Strengths  

- Works well for users whose genre and mood align with multiple songs in the catalog (e.g., lofi/chill, pop/happy). The Chill Studier profile consistently received quiet, acoustic lofi tracks that matched expectations.
- The scoring is fully transparent — every recommendation comes with a breakdown showing exactly how many points each factor contributed. Users can see *why* a song was recommended, unlike black-box systems.
- Handles extreme preferences gracefully. The All-Zeros and All-Ones edge cases both produced reasonable results because the continuous similarity formula degrades smoothly rather than breaking at boundaries.
- The configurable weight system (Choice 0/1/2) makes it easy to experiment with different scoring philosophies and observe the impact immediately.

---

## 6. Limitations and Bias 

The system creates a **single-song genre lock** for most users: 15 out of 17 genres in the catalog have only one song, and the +2.0 genre weight is so dominant that this lone representative is virtually guaranteed to rank #1 regardless of the user's energy, mood, or valence preferences. Our adversarial testing confirmed this — in Edge Case 7 (Pop Fan with Metal Tastes), a user whose numeric preferences perfectly matched metal music still got two pop songs ranked above the actual metal track, because the genre bonus alone outweighed near-perfect alignment on every other feature. This means users of single-song genres receive the illusion of personalization when the outcome is effectively pre-determined. The filter bubble is invisible to the user: the system never signals that only one song in the catalog matched their genre, so they have no reason to question the recommendation.  

---

## 7. Evaluation  

We tested the recommender against **4 standard profiles** and **7 adversarial edge-case profiles**.

**Standard profiles tested:**
- **Pop Enthusiast** (pop, happy, energy 0.8) — top pick was "Sunrise City," which felt right for an upbeat pop listener.
- **Chill Studier** (lofi, chill, energy 0.38) — top picks were "Library Rain" and "Midnight Coding," both quiet lofi tracks. Matched expectations.
- **Workout Warrior** (edm, energetic, energy 0.93) — "Digital Dreamscape" ranked #1. High-energy EDM made sense for a gym session.
- **Melancholic Folkster** (folk, melancholic, energy 0.3) — "Ghost in the Garden" dominated at 6.46. The only folk song, so it was a guaranteed winner.

**Adversarial profiles tested (7 edge cases):** Ghost Genre, All-Zeros Minimalist, All-Ones Maximalist, Acoustic EDM Fan, Mr. Average, Anti-Acoustic Chiller, and Pop Fan with Metal Tastes. These were designed with conflicting or extreme preferences to stress-test the scoring logic.

**What surprised us:**
- The **Anti-Acoustic Chiller** was the most surprising result. A user who explicitly set `likes_acoustic: False` received two highly acoustic songs (acousticness 0.86 and 0.71) as their top recommendations. We expected the system to at least deprioritize acoustic tracks, but it turned out `likes_acoustic: False` has literally zero effect — there is no penalty, only a bonus.
- The **Pop Fan with Metal Tastes** profile showed that a user with perfect numeric alignment to metal (energy 0.97, valence 0.22, aggressive mood) still got two pop songs ranked above the actual metal track. The +2.0 genre bonus overrode perfect similarity on every continuous feature.

**Logic experiment:** We ran two weight variations — Choice 1 (genre halved to 1.0, energy doubled to 3.0) and Choice 2 (mood disabled). Choice 1 improved cross-genre discovery; for example, the Workout Warrior profile started surfacing "Velvet Thunder" (hip hop, energetic) at #2, which felt musically intuitive. Choice 2 collapsed distinctions between same-genre songs, making rankings feel arbitrary.

See [reflection.md](reflection.md) for detailed profile-pair comparisons.

---

## 8. Future Work  

- **Use ML libraries or model APIs:** Replace the hand-tuned scoring weights with a learned model (e.g., scikit-learn or a Claude API call) that could discover feature importance from user feedback data rather than relying on manually chosen weights.
- **Add tempo to scoring:** The BPM data exists but is unused. Adding tempo similarity would help distinguish slow ambient tracks from fast dance music within the same energy range.
- **Introduce diversity constraints:** Instead of returning the top 5 by score alone, ensure the results include at least 2 different genres or artists to break the single-song genre lock and reduce filter bubbles.
- **Semantic similarity for genres and moods:** Replace exact string matching with embeddings or a similarity map so that "indie pop" gets partial credit against "pop," and "chill" gets partial credit against "relaxed."

---

## 9. Personal Reflection  

My biggest learning moment during this project was understanding the core algorithms behind how a music recommender works — specifically the difference between collaborative filtering (finding patterns across many users) and content-based filtering (matching song attributes to user preferences). Building one from scratch made these concepts concrete rather than abstract.

AI tools helped me code and write faster throughout the process. I was able to verify the outputs, catch issues quickly, and iterate on experiments without getting stuck on boilerplate. The speed boost let me focus more on analysis and less on syntax.

What surprised me most was that I didn't need any ML library like scikit-learn for this project. I expected to import models and train on data like in the previous project, but the entire recommender is purely math — weighted differences and simple comparisons. Yet the results still *feel* like real recommendations. That was eye-opening: even a basic formula with hand-tuned weights can produce outputs that seem intelligent, which made me realize how much of what we perceive as "smart" recommendations might be simpler than we think.

If I extended this project, I'd explore whether using an ML library or even a model API (like Claude) could learn better weights from user feedback data instead of me guessing them manually. I'd also want to study how real Spotify works under the hood — how they blend collaborative and content-based signals, handle cold-start problems, and balance personalization against discovery.
