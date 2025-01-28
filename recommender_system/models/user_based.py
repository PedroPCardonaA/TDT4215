import polars as pl
import numpy as np

class CollaborativeReccomender:
    def __init__(self, impressions: pl.DataFrame, items: pl.DataFrame, scroll_percentage_weight = 1, read_time_weight = 1):
        '''
        Initialize the CollaborativeReccomender with a user-item dataframe.

        Parameters
        ----------
        TODO fix
        '''
        self.impressions = impressions
        self.items = items
        self.cosine_vector = None
        
        # Scoring weights 
        # TODO Perhaps add articles_clicked?
        # TODO Tweak for best results
        self.scroll_percentage_weight = scroll_percentage_weight
        self.read_time_weight = read_time_weight


    def add_impression_scores(self) -> pl.DataFrame:
        '''
        Creates a score based on the user's behavior (scroll percentage and read time). Using the formula:
        impression_score = (scroll_percentage * scroll_percentage_weight) + (read_time * read_time_weight)

        Returns
        -------
        pl.DataFrame
            A DataFrame with an additional column `impression_score`.
        '''
        self.impressions = self.impressions.with_columns(
            (
                pl.col("scroll_percentage") * self.scroll_percentage_weight +
                pl.col("read_time") * self.read_time_weight
            ).alias("impression_score")
        )
        return self.impressions

    def cosine_similarity(self, user1_score: np.ndarray, user2_score: np.ndarray) -> float:
        '''
        Calculate the cosine similarity between two vectors.

        Parameters
        ----------
        user1_score : np.ndarray
            A numpy array representing the behavior of user 1.
        user2_score : np.ndarray
            A numpy array representing the behavior of user 2.

        Returns
        -------
        float
            The cosine similarity score between the two vectors. Ranges from -1 to 1.
        '''
        # Compute dot product
        dot_product = np.dot(user1_score, user2_score)
        
        # Compute norms
        norm_u = np.linalg.norm(user1_score)
        norm_v = np.linalg.norm(user2_score)
        
        # Handle division by zero (return 0 if either vector is zero)
        if norm_u == 0 or norm_v == 0:
            return 0.0
        
        # Calculate cosine similarity
        return dot_product / (norm_u * norm_v)

    def fit(self):
        '''
        Creates a user-user cosine similarity matrix and uses this to 

        Prepares user and item profiles by computing average user feature vectors
        (user_profiles) and unique item feature vectors (item_profiles).
        Also calculates norms for each user and item vector to speed up
        cosine similarity.
        '''
        self.add_impression_scores()

        return self.impressions

    def predict(self, user_id: int, article_id: int) -> float:
        
        return 0.0