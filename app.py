import streamlit as st
import pickle
import requests
import random
import time

# -----------------------------
# Load data
# -----------------------------
data = pickle.load(open('movies.pkl', 'rb'))
movies_list = data['title'].values
cosine_sim = pickle.load(open('similarity.pkl', 'rb'))

# -----------------------------
# Funny fetching messages
# -----------------------------
funny_messages = [
    "🚀 Mars se fetch kar raha hu… thoda sabar karo!",
    "🕵️ Dund raha hu bhai… almost milne wala hai!",
    "🛸 Alien network detect hua… connect kar raha hu!",
    "⏳ Loading… patience rakho yaar 😅",
    "🐢 Turtle speed se fetch kar raha hu… 🐢💨",
    "🌌 Universe me posters khoj raha hu…",
    "🤯 Poster kisi aur dimension me gaya… dhoondh raha hu!",
    "🪐 Saturn ke orbit se fetch kar raha hu… almost done!",
    "🧙 Spell cast kar raha hu… abracadabra!",
    "🤖 Robot kaam pe lag gaya… poster aa raha hai 🤖",
    "🏹 Arrow aim kiya… poster target kar liya jayega!",
    "📡 Outer space se scanning kar raha hu…",
    "🏝️ Poster desert island me phas gaya… rescue kar raha hu!",
    "🧩 Puzzle pieces assemble kar raha hu… poster aa raha hai…",
    "🎢 Fetching poster… thrill ride shuru ho gayi!"
]

# -----------------------------
# Fetch poster function
# -----------------------------
DEFAULT_POSTER = None

def fetch_poster(movie_id, placeholder):
    # Show a random funny fetching message while fetching
    placeholder.markdown(f"<p style='color:#00FF00; font-family:Courier New; font-weight:bold; font-size:20px;'>{random.choice(funny_messages)}</p>", unsafe_allow_html=True)
    time.sleep(0.10)  # simulate network delay
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=37762fdc01e2c69cb76ef60d011d32d9&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data_json = response.json()
        poster_path = data_json.get('poster_path')
        if poster_path:
            placeholder.empty()  # clear the message
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception as e:
        print(f"⚠️ Error fetching poster for {movie_id}: {e}")
    placeholder.empty()
    return DEFAULT_POSTER

# -----------------------------
# Recommendation function
# -----------------------------
def recommendation_movies(movie_name, cosine_sim, df, top_n=12):
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        return ['Movie not found in dataset!'], []

    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    recommended_movies = []
    recommended_movies_poster = []

    for i, _ in sim_scores:
        movie_row = df.iloc[i]
        recommended_movies.append(movie_row.title)
        # Create a placeholder for funny fetching message
        placeholder = st.empty()
        poster_url = fetch_poster(movie_row.id, placeholder)
        recommended_movies_poster.append(poster_url)

    return recommended_movies, recommended_movies_poster

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation 🎬")

selected_movie_name = st.selectbox(
    "Choose a movie:",
    movies_list
)

if st.button("Recommend Movies"):
    names, posters = recommendation_movies(selected_movie_name, cosine_sim, data, top_n=12)

    if names[0] == 'Movie not found in dataset!':
        st.warning(names[0])
    else:
        st.subheader(f"Recommendations for **{selected_movie_name}**:")

        # 4 rows x 3 columns layout
        card_height = "300px"
        card_width = "100%"

        for row in range(4):
            cols = st.columns([1,1,1], gap="large")
            for col_idx, col in enumerate(cols):
                idx = row * 3 + col_idx
                if idx < len(names):
                    with col:
                        if posters[idx]:
                            st.image(posters[idx], use_container_width=True)
                        else:
                            # Poster missing card
                            st.markdown(
                                f"""
                                <div style='
                                    width:{card_width};
                                    height:{card_height};
                                    border-radius:15px;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    font-size:22px;
                                    font-weight:bold;
                                    font-family: "Courier New", monospace;
                                    color:#00FF00;
                                    background-color:#000000;
                                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                    text-align:center;
                                '>
                                    Oops! Poster Not Available ❌🎬😢
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        # Movie title below card
                        st.markdown(
                            f"<p style='text-align:center; font-size:18px; font-weight:bold; margin-top:10px;'>🎞️ {names[idx]}</p>",
                            unsafe_allow_html=True
                        )
