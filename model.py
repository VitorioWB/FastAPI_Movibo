import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Carregar o DataFrame
df = pd.read_csv("imdb_top_1000.csv")

# Preencher valores NaN com a média das colunas
df['IMDB_Rating'] = df['IMDB_Rating'].fillna(df['IMDB_Rating'].mean())
df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].mean())

# Normalizar as colunas necessárias para clustering
scaler = StandardScaler()
df[['IMDB_Rating', 'Meta_score']] = scaler.fit_transform(df[['IMDB_Rating', 'Meta_score']])

# Criar o modelo de clustering
kmeans = KMeans(n_clusters=10, random_state=42)
df['Cluster'] = kmeans.fit_predict(df[['IMDB_Rating', 'Meta_score']])

# Função para recomendar filmes
def recommend_movies(title, n_recommendations=5):
    # Encontrar o filme no DataFrame
    movie = df[df['Series_Title'].str.contains(title, case=False, na=False)]
    if movie.empty:
        return None
    
    movie = movie.iloc[0]
    cluster = movie['Cluster']
    genres = movie['Genre'].split(', ')
    
    # Filtrar filmes do mesmo cluster e que compartilhem pelo menos dois gêneros
    recommendations = df[
        (df['Cluster'] == cluster) &
        (df['Genre'].apply(lambda x: sum(genre in x for genre in genres) >= 2))
    ]
    
    # Remover o filme original das recomendações
    recommendations = recommendations[recommendations['Series_Title'] != movie['Series_Title']]
    
    # Ordenar por popularidade e pegar as top recomendações
    recommendations = recommendations.sort_values(by=['IMDB_Rating', 'Meta_score'], ascending=False)
    recommendations = recommendations.head(n_recommendations)
    
    return recommendations
