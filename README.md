# playlist-clustering
A machine learning model to suggest playlists for a set of songs based on similarity. This project uses Principal Component Analysis (PCA) and Gaussian Mixture Models (GMM) to extract the most important features from each song and cluster a list of songs into unique groups or playlists.

## Prerequisites
To run this project, you will need to have the following dependencies installed:

* NumPy
* SciPy
* scikit-learn
* spotipy

You can install these dependencies using pip:

```
pip install numpy scipy scikit-learn spotipy
```
  
## Usage
To use this project, first clone the repository and navigate to the project directory:

```bash
git clone https://github.com/your-username/playlist-clustering.git
cd playlist-clustering
```

I would recommend opening the Jupyter notebook playlist_clustering.ipynb and playlist_clustering_tiktok.ipynb to see a detailed explanation and visualization of the playlist classification process.

To create new playlists based on the model, run the create_playlists.py script and update create_playlists.py client id and secret token fields to authenticate with your Spotify account and import your user playlists.

```bash
python create_playlists.py
```

License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
