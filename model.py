import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Carregar a base de dados
df = pd.read_csv('imdb_top_1000.csv')

# Função para treinar o modelo e adicionar clusters ao DataFrame
def train_model():
    # Selecionar features e remover nulos
    features = df[['IMDB_Rating', 'Meta_score']].dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Treinar o modelo KMeans
    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(scaled_features)
    
    # Adicionar os clusters de volta ao DataFrame original
    df.loc[features.index, 'Cluster'] = kmeans.labels_
    return df

# Treinar o modelo ao importar este módulo
df = train_model()
