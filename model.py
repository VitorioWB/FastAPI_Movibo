import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

# Carregar a base de dados
df = pd.read_csv('imdb_top_1000.csv')

def train_model():
    features = df[['IMDB_Rating', 'Meta_score']].dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(scaled_features)
    
    df.loc[features.index, 'Cluster'] = kmeans.labels_
    joblib.dump(kmeans, 'kmeans_model.pkl')
    return df

def load_model():
    global df
    try:
        kmeans = joblib.load('kmeans_model.pkl')
        features = df[['IMDB_Rating', 'Meta_score']].dropna()
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        df.loc[features.index, 'Cluster'] = kmeans.predict(scaled_features)
    except FileNotFoundError:
        df = train_model()
    return df

df = load_model()
