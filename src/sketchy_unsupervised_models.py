'''
Project Name: Sketchy Parking Lot
Authors: Joey Garcia and Reilly Rodriguez Spencer

Purpose: Run k-means clustering and isolation forest anomaly detection on the Parked Pages dataset.
'''

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class UnsupervisedSketchyModels:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.kmeans_model = None
        self.isolation_forest_model = None
        self.scaler = StandardScaler()
        self.X_scaled = None

        # Engineered feature columns to use for modeling
        self.feature_cols = [
            "ad_score",
            "parked_score",
            "suspicious_score",
            "num_redirects",
            "avg_redirect_jaccard",
            "min_redirect_jaccard",
            "low_redirect_similarity_flag",
            "first_last_redirect_similarity",
            "lang_tld_mismatch"
        ]
    
    def fit_kmeans(self, n_clusters=3):
        X = self.df[self.feature_cols].fillna(0)
        self.X_scaled = self.scaler.fit_transform(X)

        self.kmeans_model = KMeans(
            n_clusters=n_clusters,
            random_state=1
        )
        
        self.df["kmeans_cluster"] = self.kmeans_model.fit_predict(self.X_scaled)
        
        return self.df
    
    def fit_isolation_forest(self, n_estimators=100, contamination=0.01):
        if self.X_scaled is None:
            X = self.df[self.feature_cols].fillna(0)
            self.X_scaled = self.scaler.fit_transform(X)

        self.isolation_forest_model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=1
        )

        self.isolation_forest_model.fit(self.X_scaled)
        
        # Raw anomaly score (higher = more normal)
        raw_scores = self.isolation_forest_model.decision_function(self.X_scaled)
        # Convert to threat score (higher = more risky)
        self.df["iforest_score"] = -raw_scores
        # normalize to 0-100
        self.df["iforest_score_normalized"] = self.normalize_score(self.df["iforest_score"])

        return self.df

    def normalize_score(self, x):
        return 100 * (x - x.min()) / (x.max() - x.min())
