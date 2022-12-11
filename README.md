# playlist-clustering
Model to suggest playlists for a set of songs based on similarity

1. User defined # of playlists vs automated #?
2. Playlist clustering could be more useful when not considering genres, because using genres is such an important factor in playlist cohesion. Consider refactoring to optimize around first splitting up by genre and then splitting up by playlist ? Or engineering feature such that genre has much more "weight" than other features
3. Could we add support for interacting with Spotify API to import "liked" songs, or current playlists which have gotten too large so that the playlist clustering model is more straightforward to use?
