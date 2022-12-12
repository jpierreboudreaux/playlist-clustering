import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
from playlist_generator import PlaylistGenerator

def spotify_setup():
    """
    Set up the Spotify client with the necessary authentication and scopes.
    Returns the client object, the user's ID, and a list of the user's playlists.
    """
    scopes = ["user-read-private","playlist-read-private","playlist-read-collaborative","playlist-modify-private","user-library-read"]
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    redirect_uri = "your_redirect_url"

    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scopes)
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    user_id = sp.current_user()["id"]
    user_playlists = sp.user_playlists(user_id)["items"]
    return spotify, user_id, user_playlists

def get_playlist_to_split():
    """
    Prompt the user to input the name of the playlist they want to split up.
    Return the playlist's ID.
    """
    while True:
        user_input = input("Which playlist would you like to split up ?\n")
        for playlist in user_playlists:
            if playlist["name"] == user_input:
                return playlist["id"]
        print("Playlist name not recognized.")

def get_num_playlists():
    """
    Prompt the user to input the desired number of playlists. If no input is given,
    return 3 as the default number of playlists.
    """
    user_input = input("Desired number of playlists: (Leave blank to automate)\n")
    if not user_input or not user_input.isdigit():
        user_input = "3"
    return int(user_input)

def pandas_setup(sp):
    """
    Set up a Pandas dataframe with information about the tracks in the selected playlist.
    Return the original dataframe and a reduced version of the dataframe with only relevant columns.
    """
    user_tracks = sp.user_playlist_tracks(user_id, playlist_id)["items"]
    tracks = map(lambda x : x["track"], user_tracks)
    data = pd.DataFrame(tracks)

    # drop unnecessary columns
    data_reduced = data.drop(columns=["artists","available_markets","disc_number","episode","explicit",
    "external_ids","external_urls","href","id","name","preview_url","track","track_number","type","uri"])

    # TODO: Fix extraction of album columns
    # unwrap "album" column into multiple new columns + drop some of those
        # result_df = json_normalize(df, dict_column_name, meta=['other', 'columns'])
    # album_data = data_reduced["album"].apply(pd.Series) # pylint: disable=E1136  # pylint/issues/3139
    # album_data.drop(columns=["artists","available_markets","external_urls","href","id","images",
    # "release_date_precision","total_tracks","type","uri"], inplace=True)
    data_reduced.drop(columns=["album"], inplace=True)
    # data_reduced = album_data.join(data_reduced, lsuffix="album")

    return data, data_reduced

def generate_playlists(data, data_reduced, n_playlists):
    """
    Generate a specified number of playlists by grouping the tracks in the given dataframe.
    Return a dictionary with the playlist number as the key and a list of track URIs as the value.
    """
    playlist_generator = PlaylistGenerator(data_reduced)
    playlist_nums = playlist_generator.generate(num_playlists=n_playlists)

    # group songs by playlist
    playlists = {key : [] for key in np.unique(playlist_nums)}
    for i, playlist_num in enumerate(playlist_nums):
        playlists[playlist_num].append(data.loc[i, "uri"])
    return playlists

def create_spotify_playlists(user_id, playlists):
    """
    Create new Spotify playlists for each group of tracks and add the tracks to each playlist.
    """
    desc = "This playlist was created by an ensemble of machine learning models!"
    for track_list in playlists.values():
        user_input = input("Give a random playlist name!\n")
        new_playlist = sp.user_playlist_create(user_id, user_input, public=False, description=desc)
        new_playlist_id = new_playlist["id"]
        sp.user_playlist_add_tracks(user_id, new_playlist_id, track_list)

# scripting
sp, user_id, user_playlists = spotify_setup()
playlist_id = get_playlist_to_split()
num_playlists = get_num_playlists()
data, reduced_data = pandas_setup(sp)
my_playlists = generate_playlists(data, reduced_data, num_playlists)
create_spotify_playlists(user_id, my_playlists)