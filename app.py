import os
import subprocess
import streamlit as st

# Build model automatically if it doesn't exist
if not os.path.exists("models/similarity.pkl"):
    st.info("Building recommendation model for first run... Please wait ⏳")

    result = subprocess.run(
        ["python", "models/build_model.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Model build failed!")
        st.code(result.stderr)
        st.stop()

# 👇 YE LINE YAHAN HOGI (subprocess ke bahar)
from recommender import recommend

if result.returncode != 0:
    st.error("Model build failed!")
    st.code(result.stderr)
    st.stop()

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="AI Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>

.stApp{
    background:#0E1117;
}

h1{
    text-align:center;
    color:#E50914;
    font-size:55px;
}

.stButton>button{
    width:100%;
    height:55px;
    background:#E50914;
    color:white;
    font-size:20px;
    font-weight:bold;
    border-radius:10px;
}

.stButton>button:hover{
    background:#B20710;
    color:white;
}

img{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# Title
# -----------------------

st.title("🎬 AI Movie Recommendation System")

st.write(
"### Get movie recommendations using Machine Learning, NLP and TMDB API"
)

movie = st.text_input("Enter Movie Name")

if st.button("Recommend Movies"):

    with st.spinner("Finding similar movies..."):

        names, posters = recommend(movie)

    if len(names) == 0:

        st.error("Movie not found!")

    else:

        st.subheader("🔥 Recommended Movies")

        cols = st.columns(5)

        for i in range(5):

            with cols[i]:

                st.image(posters[i])

                st.markdown(
                    f"<h4 style='text-align:center'>{names[i]}</h4>",
                    unsafe_allow_html=True
                )

st.markdown("---")
st.caption("Made with ❤️ using Python | Machine Learning | Streamlit | TMDB API")