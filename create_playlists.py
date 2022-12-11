import pandas as pd
import spotify

from playlist_generator import PlaylistGenerator

# determine number of playlists
user_input = input("Desired number of playlists: (Leave blank to automate)")
if not user_input or not user_input.isdigit():
    user_input = "3"
num_playlists = int(user_input)

# set-up spotify API
spotify_client = spotify.Client(access_token='INSERT_ACCESS_TOKEN_HERE')
spotify_data = spotify_client.playlist('YOUR_PLAYLIST_ID')

# set-up pandas dataframe
data = pd.DataFrame(spotify_data)
data.drop(columns=["track_pop","album","artist_pop"], inplace=True)

artists = data["artist_name"].unique()
data["artist_name"] = data["artist_name"].factorize()[0]

songs = data["track_name"]
data.drop("track_name", axis=1, inplace=True) # pylint: disable=E1101

# invoke playlist generator
playlist_generator = PlaylistGenerator(data)
playlists = playlist_generator.generate(3)

# add old and new features
data["playlist"] = playlists
data["track_name"] = songs

# group songs by playlist
playlist_dict = dict(tuple(data.groupby("playlist")))