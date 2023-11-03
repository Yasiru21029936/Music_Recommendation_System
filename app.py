import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Your Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define your login credentials
valid_username = "user"
valid_password = "user"

# Function to authenticate the user
def login():
    st.title('Music Recommender System')
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == valid_username and password == valid_password:
            return True
        else:
            st.error("Invalid credentials. Please try again.")
            return False

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names,recommended_music_posters

# Main application
if 'login_state' not in st.session_state:
    st.session_state.login_state = False

if not st.session_state.login_state:
    if login():
        st.session_state.login_state = True
else:
    st.write("Welcome to the Music Recommender System")

    st.write("Select a song from the dropdown and click 'Show Recommendation' to get music recommendations.")

    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    music_list = music['song'].values
    selected_song = st.selectbox("Select a song", music_list)

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters = recommend(selected_song)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_music_names[0] if recommended_music_names else "No recommendations")
            st.image(recommended_music_posters[0] if recommended_music_posters else "")
        with col2:
            st.text(recommended_music_names[1] if recommended_music_names else "")
            st.image(recommended_music_posters[1] if recommended_music_posters else "")
        with col3:
            st.text(recommended_music_names[2] if recommended_music_names else "")
            st.image(recommended_music_posters[2] if recommended_music_posters else "")
        with col4:
            st.text(recommended_music_names[3] if recommended_music_names else "")
            st.image(recommended_music_posters[3] if recommended_music_posters else "")
        with col5:
            st.text(recommended_music_names[4] if recommended_music_names else "")
            st.image(recommended_music_posters[4] if recommended_music_posters else "")
