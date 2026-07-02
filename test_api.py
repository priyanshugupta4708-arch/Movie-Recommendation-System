import requests
import pickle

API_KEY = "a1d8428b743b8f0449d54b2cae2cbe47"

url = "https://api.themoviedb.org/3/search/movie"

params = {
    "api_key": API_KEY,
    "query": "Iron Man"
}

try:
    r = requests.get(url, params=params, timeout=10)
    print("Status:", r.status_code)
    print(r.json()["results"][0]["poster_path"])
except Exception as e:
    print("ERROR:", e)

movies = pickle.load(open("models/movies.pkl", "rb"))

print(movies[movies["title"] == "Iron Man 3"])