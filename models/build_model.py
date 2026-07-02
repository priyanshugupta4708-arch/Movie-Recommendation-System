import pandas as pd
import ast
import pickle


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===========================
# Load datasets
# ===========================

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

print("============== COLUMNS ==============")
print(movies.columns.tolist())
print("====================================")

# Select required columns
movies = movies[
    [
        "movie_id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew",
        
    ]
]

# Remove missing values
movies.dropna(inplace=True)

# ===========================
# Helper Functions
# ===========================

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L


def convert3(obj):
    L = []
    counter = 0

    for i in ast.literal_eval(obj):
        if counter < 3:
            L.append(i["name"])
            counter += 1
        else:
            break

    return L


def fetch_director(obj):
    L = []

    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break

    return L


def collapse(L):
    L1 = []

    for i in L:
        L1.append(i.replace(" ", ""))

    return L1


# ===========================
# Feature Engineering
# ===========================

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert3)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

movies["genres"] = movies["genres"].apply(collapse)
movies["keywords"] = movies["keywords"].apply(collapse)
movies["cast"] = movies["cast"].apply(collapse)
movies["crew"] = movies["crew"].apply(collapse)

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# ===========================
# New DataFrame
# ===========================

new_df = movies[['movie_id', 'title', 'tags']]

new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

# ===========================
# Vectorization
# ===========================

cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(new_df["tags"]).toarray()

# ===========================
# Similarity Matrix
# ===========================

similarity = cosine_similarity(vectors)

# ===========================
# Save Model
# ===========================

pickle.dump(new_df, open("models/movies.pkl", "wb"))
pickle.dump(similarity, open("models/similarity.pkl", "wb"))

print("=" * 50)
print("Model Built Successfully!")
print("=" * 50)
print("Movies Shape :", new_df.shape)
print("Similarity Shape :", similarity.shape)
print("Files Saved:")
print("- models/movies.pkl")
print("- models/similarity.pkl")