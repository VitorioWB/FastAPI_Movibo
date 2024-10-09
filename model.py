import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Carregar o DataFrame
df = pd.read_csv("imdb_top_1000.csv")

# Preencher valores NaN com a média das colunas
df['IMDB_Rating'] = df['IMDB_Rating'].fillna(df['IMDB_Rating'].mean())
df['Meta_score'] = df['Meta_score'].fillna(df['Meta_score'].mean())

# Criar uma cópia do DataFrame para normalização e clustering
df_clustering = df.copy()

# Normalizar as colunas necessárias para clustering
scaler = StandardScaler()
df_clustering[['IMDB_Rating', 'Meta_score']] = scaler.fit_transform(df_clustering[['IMDB_Rating', 'Meta_score']])

# Criar o modelo de clustering
kmeans = KMeans(n_clusters=10, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_clustering[['IMDB_Rating', 'Meta_score']])

# Função de recomendação avançada
def recommend_movies_advanced(title=None, description=None, genres=None, n_recommendations=3):
    # Inicializar recomendações
    recommendations = pd.DataFrame()

    # Filtros com base nos critérios fornecidos
    if title:
        recommendations = df[df['Series_Title'].str.contains(title, case=False, na=False)]

    if description:
        description_results = df[df['Overview'].str.contains(description, case=False, na=False)]
        recommendations = pd.concat([recommendations, description_results])

    if genres:
        genres_set = set(genres.split(', '))
        # Corrigido para retornar True ou False com base na interseção de gêneros
        genre_results = df[df['Genre'].apply(lambda x: len(genres_set.intersection(set(x.split(', ')))) > 0)]
        recommendations = pd.concat([recommendations, genre_results])

    if recommendations.empty:
        return None

    # Filtra para remover filmes com o mesmo título ou derivados, caso o nome tenha sido fornecido
    if title:
        recommendations = recommendations[~recommendations['Series_Title'].str.contains(title, case=False, na=False)]

    # Remove duplicados após combinar múltiplos critérios
    recommendations = recommendations.drop_duplicates(subset=['Series_Title'])

    # Se não houver recomendações suficientes, seleciona filmes aleatórios do mesmo cluster
    if len(recommendations) < n_recommendations and title:
        base_movie_cluster = df[df['Series_Title'].str.contains(title, case=False, na=False)]
        if not base_movie_cluster.empty:
            cluster = base_movie_cluster.iloc[0]['Cluster']
            cluster_recommendations = df[(df['Cluster'] == cluster) & ~df['Series_Title'].str.contains(title, case=False, na=False)]
            additional_recommendations = cluster_recommendations.sample(n=n_recommendations - len(recommendations))
            recommendations = pd.concat([recommendations, additional_recommendations])

    # Ordenar por popularidade e pegar as top recomendações
    recommendations = recommendations.sort_values(by=['IMDB_Rating', 'Meta_score'], ascending=False)
    recommendations = recommendations.head(n_recommendations)

    return recommendations
