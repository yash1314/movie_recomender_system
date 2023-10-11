import time
import streamlit as st
import joblib
import requests

movies = joblib.load('models/movie.pkl')
similarity = joblib.load('models/similarity.pkl')
movies_lst = movies['title'].values

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=2771a082cbd055cd97360da72184d41e&language=en-US".format(movie_id)
    response = requests.get(url=url)
    data = response.json()
    poster_path = data['poster_path']
    final_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return final_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    result = sorted(list(enumerate(distances)), reverse=True, key= lambda x:x[1])[1:5]

    recommended_movies_names = []
    recommended_movies_poster = []
    for i in result:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
    return recommended_movies_names, recommended_movies_poster

st.title('Movie Recommendation System')
st.markdown(" ")
selected_movie_name = st.selectbox('Select any movie', movies_lst)

if st.button('**Recommend**'):
    bar = st.progress(30)
    time.sleep(1)
    bar.progress(60)
    rec_movies, poster = recommend(selected_movie_name)
    bar.progress(100)

    col0, col1, col2, col3 = st.columns(4)

    with col0:
        st.text(rec_movies[0])
        st.markdown(" ")
        st.image(poster[0])

    with col1:
        st.text(rec_movies[1])
        st.markdown(" ")
        st.image(poster[1])

    with col2:
        st.text(rec_movies[2])
        st.markdown(" ")
        st.image(poster[2])

    with col3:
        st.text(rec_movies[3])
        st.markdown(" ")
        st.image(poster[3])

