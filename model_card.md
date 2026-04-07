# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
