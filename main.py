import os
import unicodedata
import pandas as pd
from fastapi import FastAPI, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from model import recommend_movies_advanced
from utils import format_movie, generate_recommendation_message


# Função para remover acentos e transformar o texto em minúsculas
def normalize_text(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()


# Carregar os datasets
df_full = pd.read_csv('imdb_top_1000.csv')  # Dataset completo para recomendações gerais
df_keywords = pd.read_csv('imdb_top_5_with_keywords_pt.csv')  # Dataset reduzido para busca por descrição

# Aplicar normalização apenas no dataset df_keywords
df_keywords['Series_Title'] = df_keywords['Series_Title'].apply(normalize_text)
df_keywords['Genre'] = df_keywords['Genre'].apply(normalize_text)
df_keywords['Overview'] = df_keywords['Overview'].apply(normalize_text)
df_keywords['keywords'] = df_keywords['keywords'].apply(normalize_text)

stop_words = ["the", "and", "to", "a", "in", "of", "is", "on", "o", "a", "e", "de", "do", "da"]

# Configuração do FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {
        "message": (
            "Bem-vindo ao FastAPI Movibo!\n\n"
            "Você pode usar o endpoint '/recomendados/' para obter recomendações de filmes com base em diferentes critérios."
            "\n\nNovo endpoint: '/buscar_por_descricao/' para encontrar filmes por uma breve descrição."
        )
    }

# main.py
@app.get("/recomendados/")
def recommend_movies_endpoint(title: str = None, genres: str = None, description: str = None):
    if not title and not genres and not description:
        raise HTTPException(status_code=400, detail="Pelo menos um parâmetro ('title', 'genres', 'description') é obrigatório.")

    # Chamando a função de recomendação usando o dataset completo
    recommendations = recommend_movies_advanced(
        title=title,
        description=description,
        genres=genres,
        n_recommendations=3
    )
    
    if recommendations is None or recommendations.empty:
        recommendations = df_full.sample(3)
        generic_message = "Não encontramos filmes que correspondam exatamente aos critérios fornecidos. Aqui estão algumas recomendações genéricas:"
    else:
        generic_message = "Recomendado com base nos critérios fornecidos."

    formatted_recommendations = [format_movie(movie) for _, movie in recommendations.iterrows()]
    recommendation_messages = []
    
    return {
        "title": title if title else "Não fornecido",
        "genres": genres if genres else "Não fornecido",
        "description": description if description else "Não fornecido",
        "recommendations": formatted_recommendations,
        "messages": recommendation_messages if recommendation_messages else [generic_message]
    }



@app.get("/buscar_por_descricao/")
def search_movie_by_description(description: str):
    if not description:
        raise HTTPException(status_code=400, detail="A descrição é obrigatória.")

    # Normalizar a descrição fornecida pelo usuário
    description = normalize_text(description)
    
    # Configuração do TF-IDF com uma lista personalizada de stop words
    vectorizer = TfidfVectorizer(max_features=200, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(df_keywords['keywords'])

    # Vetorizar a descrição fornecida
    description_vector = vectorizer.transform([description])

    # Calcular a similaridade de cosseno
    similarity_scores = cosine_similarity(description_vector, tfidf_matrix).flatten()
    most_similar_index = similarity_scores.argmax()

    # Verifique se a similaridade é suficiente para considerar uma correspondência
    if similarity_scores[most_similar_index] == 0:
        raise HTTPException(status_code=404, detail="Nenhum filme correspondente encontrado.")

    # Seleciona o filme mais similar
    most_similar_movie = df_keywords.iloc[most_similar_index]

    return {
        "Title": most_similar_movie['Series_Title'],
        "Genre": most_similar_movie['Genre'],
        "Director": most_similar_movie['Director'],
        "IMDB_Rating": most_similar_movie['IMDB_Rating'],
        "Meta_score": most_similar_movie['Meta_score'],
        "Description": most_similar_movie['Overview'],
        "Poster_Link": most_similar_movie['Poster_Link']
    }




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
