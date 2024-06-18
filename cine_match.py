import streamlit as st
import pandas as pd

class CineMatch:
    def __init__(self):
        if 'movies' not in st.session_state:
            st.session_state['movies'] = []
    
    def add_movie(self, title, genre, rating, language, production):
        # Check for duplicate movies
        for movie in st.session_state['movies']:
            if (movie['title'].lower() == title.lower() and
                movie['genre'].lower() == genre.lower() and
                movie['language'].lower() == language.lower() and
                movie['production'].lower() == production.lower()):
                # Update the rating by averaging
                movie['rating'] = (movie['rating'] + rating) / 2
                st.success(f"Movie '{title}' already exists. Updated the rating to {movie['rating']:.1f}.")
                return

        # If no duplicate, add the new movie
        movie = {
            'title': title,
            'genre': genre,
            'rating': rating,
            'language': language,
            'production': production
        }
        st.session_state['movies'].append(movie)
        st.success(f"Movie '{title}' added successfully.")
    
    def search_by_title(self, title):
        return [movie for movie in st.session_state['movies'] if title.lower() in movie['title'].lower()]
    
    def search_by_genre(self, genre):
        return [movie for movie in st.session_state['movies'] if genre.lower() in movie['genre'].lower()]
    
    def search_by_language(self, language):
        return [movie for movie in st.session_state['movies'] if language.lower() in movie['language'].lower()]
    
    def filter_by_genre(self, genre):
        return [movie for movie in st.session_state['movies'] if genre.lower() in movie['genre'].lower()]
    
    def filter_by_language(self, language):
        return [movie for movie in st.session_state['movies'] if language.lower() in movie['language'].lower()]
    
    def recommend_top_n(self, n, order):
        sorted_movies = sorted(st.session_state['movies'], key=lambda x: x['rating'], reverse=(order == 'Top'))
        return sorted_movies[:n]
    
    def delete_movie(self, title):
        initial_length = len(st.session_state['movies'])
        st.session_state['movies'] = [movie for movie in st.session_state['movies'] if movie['title'].lower() != title.lower()]
        return len(st.session_state['movies']) < initial_length

# Initialize the CineMatch system
cine_match = CineMatch()

# Streamlit App
st.title("CineMatch: Movie Recommendation System")

# Add Movie Section
st.header("Add a New Movie")
title = st.text_input("Title")
genre = st.text_input("Genre")
rating = st.number_input("Rating", min_value=0.0, max_value=10.0, step=0.1)
language = st.text_input("Language")

# Predefined production options with an "Other" option
production_options = ["Bollywood", "Tollywood", "Hollywood", "Kollywood", "Mollywood", "Other"]
production = st.selectbox("Production", production_options)

if st.button("Add Movie"):
    cine_match.add_movie(title, genre, rating, language, production)

# Search Movies by Title
st.header("Search Movies by Title")
search_title = st.text_input("Search Title")
if st.button("Search by Title"):
    results = cine_match.search_by_title(search_title)
    if results:
        df = pd.DataFrame(results)
        st.table(df)
    else:
        st.warning(f"No movies found with title '{search_title}'.")

# Search Movies by Genre
st.header("Search Movies by Genre")
search_genre = st.text_input("Search Genre")
if st.button("Search by Genre"):
    results = cine_match.search_by_genre(search_genre)
    if results:
        df = pd.DataFrame(results)
        st.table(df)
    else:
        st.warning(f"No movies found with genre '{search_genre}'.")

# Search Movies by Language
st.header("Search Movies by Language")
search_language = st.text_input("Search Language")
if st.button("Search by Language"):
    results = cine_match.search_by_language(search_language)
    if results:
        df = pd.DataFrame(results)
        st.table(df)
    else:
        st.warning(f"No movies found with language '{search_language}'.")

# Filter Movies by Genre
st.header("Search Movies by Production")
filter_production = st.text_input("Filter by Production")
if st.button("Filter by Production"):
    filtered_results = cine_match.filter_by_production(filter_production)
    if filtered_results:
        df = pd.DataFrame(filtered_results)
        st.table(df)
    else:
        st.warning("No movies match the filter criteria for production.")


# Recommend Top N Movies
st.header("Recommend N Movies")
top_n = st.number_input("Number of Top Movies", min_value=1, step=1)
order = st.selectbox("Sort Order", ["Top", "Low"])
if st.button("Recommend"):
    recommendations = cine_match.recommend_top_n(int(top_n), order)
    if recommendations:
        df = pd.DataFrame(recommendations)
        st.table(df)
    else:
        st.warning("No movies to recommend.")

# Delete Movie by Title
st.header("Delete a Movie by Title")
delete_title = st.text_input("Delete Title")
if st.button("Delete"):
    if cine_match.delete_movie(delete_title):
        st.success(f"Movie '{delete_title}' deleted successfully.")
    else:
        st.warning(f"No movie found with title '{delete_title}'.")

# Display all movies
st.header("All Movies")
if st.session_state['movies']:
    df = pd.DataFrame(st.session_state['movies'])
    st.table(df)
else:
    st.warning("No movies available.")
