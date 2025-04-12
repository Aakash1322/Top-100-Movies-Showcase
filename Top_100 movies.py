import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Top 100 Movies", layout="wide")

# Title
st.title("🎬 Top 100 Movies Showcase")
st.markdown("Discover the best movies of all time, beautifully presented.")

url = "https://imdb-top-100-movies.p.rapidapi.com/"

headers = {
	"x-rapidapi-key": "d9e759d3c0msh2410698f0b75e5fp10a2e4jsn9f599cbbd0a8",
	"x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())


# Fetch Data
@st.cache_data
def fetch_movies():
    response = requests.get(url = "https://imdb-top-100-movies.p.rapidapi.com/"
, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch movies 😢")
        return []

movies = fetch_movies()

# Filter & Sort
st.sidebar.title("🔎 Filters")
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 8.0, 0.1)
search = st.sidebar.text_input("Search by Title")

filtered = []

for m in movies:
    try:
        rating = float(m.get("rating", 0) or 0)
        title = m.get("title", "")
        if rating >= min_rating and search.lower() in title.lower():
            filtered.append(m)
    except:
        continue  # Skip any item with bad data


# Display
cols = st.columns(3)

for idx, movie in enumerate(filtered):
    with cols[idx % 3]:
        st.image(movie.get("image", ""), width=200)
        st.markdown(f"**{movie['title']}** ({movie['year']})")
        st.markdown(f"⭐ **{movie['rating']}**")
        if movie.get("plot"):
            st.caption(movie["plot"][:100] + "...")
        st.markdown("---")