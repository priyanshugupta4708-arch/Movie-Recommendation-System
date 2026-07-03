import pickle
import requests

# ==========================
# TMDB API KEY
# ==========================
API_KEY = "a1d8428b743b8f0449d54b2cae2cbe47"

# ==========================
# Load Model
# ==========================
movies = None
similarity = None


def load_model():
    global movies, similarity

    if movies is None:
        movies = pickle.load(open("models/movies.pkl", "rb"))

    if similarity is None:
        similarity = pickle.load(open("models/similarity.pkl", "rb"))


# ==========================
# Fetch Poster
# ==========================
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://placehold.co/500x750?text=No+Poster"

    except Exception as e:
        print("Poster Error:", e)
        return "https://placehold.co/500x750?text=No+Poster"


# ==========================
# Recommend Movies
# ==========================
def recommend(movie):

    load_model()

    movie = movie.strip().lower()

    matches = movies[movies["title"].str.lower() == movie]

    if matches.empty:
        return [], []

    index = matches.index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in distances:

        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters
