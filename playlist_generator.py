from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
import pandas as pd

class PlaylistGenerator:

    def __init__(self, df):
        """
        Initialize the playlist generator using a pandas dataframe.
        """
        self.df = df

    def generate(self, num_playlists=None):
        """
        Generate the different playlists from the dataset of songs.
        Optionally, pass in the desired number of playlists as a parameter.
        """
        if num_playlists is None:
            num_playlists = len(self.df["genre"].unique())

        self.PCA()
        playlists = self.GMM(num_playlists)
        return playlists
        

    def PCA(self, n_components=4):
        """
        Perform Principal Components Analysis on the dataset to reduce
        the dimensionality to be used for GMM later.
        """
        pca = PCA(n_components=n_components)
        pca.fit(self.df)

        # reduce dataset
        self.df = pd.DataFrame(pca.transform(self.df), columns=['A', 'B', 'C', 'D'])

    def GMM(self, n_playlists):
        """
        Apply a Gaussian Mixture Model to the dataset to
        determine the different playlists
        """
        # fit the gmm model to entire songlist
        gmm = GaussianMixture(n_components=n_playlists, init_params='k-means++')
        gmm.fit(self.df)

        # classify data into separate playlists
        playlists = gmm.predict(self.df)
        return playlists