import pickle
import streamlit as st
import requests
import time

# ---------------- Fetch Poster ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    
    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster"
        except:
            time.sleep(1)  # wait before retry
    
    # final fallback
    return "https://via.placeholder.com/500x750?text=Error"

# ---------------- Recommend Movies ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .main {
            background-color: #0e1117;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #ff4b4b !important;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
        }
        .stSelectbox label {
            font-size: 18px !important;
            font-weight: bold;
            color: #f5f5f5 !important;
        }
        .movie-title {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
            color: #e5e5e5;
        }
        .stButton button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #ff1c1c;
            transition: 0.3s;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "✨ Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("<h2>🔥 Top 5 Recommendations</h2>", unsafe_allow_html=True)
    cols = st.columns(5, gap="large")

    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)
