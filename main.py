import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from model import df, recommend_movies_advanced
from utils import format_movie, generate_recommendation_message

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": (
            "Bem-vindo ao FastAPI Movibo!\n\n"
            "Você pode usar o endpoint '/recomendados/' para obter recomendações de filmes com base em diferentes critérios.\n\n"
            "**Como utilizar**:\n"
            "- Para buscar filmes por **nome**, adicione o parâmetro `?title=Nome do Filme`\n"
            "- Para buscar filmes por **gêneros**, adicione o parâmetro `?genres=Ação, Aventura` (separados por vírgula)\n"
            "- Para buscar filmes por **descrição**, adicione o parâmetro `?description=Palavra-chave ou frase`\n\n"
            "Exemplo de requisição para recomendações baseadas no nome:\n"
            "`/recomendados/?title=Inception`\n\n"
            "Exemplo de requisição para recomendações por gênero:\n"
            "`/recomendados/?genres=Action, Thriller`\n\n"
            "Exemplo de requisição para recomendações com base na descrição:\n"
            "`/recomendados/?description=dream world`\n\n"
            "Use um ou mais parâmetros combinados para refinar sua pesquisa!"
        )
    }

@app.get("/recomendados/")
def recommend_movies_endpoint(title: str = None, genres: str = None, description: str = None):
    # Verifica se pelo menos um critério foi passado
    if not title and not genres and not description:
        raise HTTPException(status_code=400, detail="Pelo menos um parâmetro ('title', 'genres', 'description') é obrigatório.")

    # Gera as recomendações com base nos critérios fornecidos
    recommendations = recommend_movies_advanced(title=title, description=description, genres=genres, n_recommendations=3)
    
    # Se não houver recomendações, selecionar 3 filmes aleatórios
    if recommendations is None or recommendations.empty:
        recommendations = df.sample(3)  # Seleciona 3 filmes aleatórios do DataFrame
        generic_message = "Não encontramos filmes que correspondam exatamente aos critérios fornecidos. Aqui estão algumas recomendações genéricas:"
    else:
        generic_message = "Recomendado com base nos critérios fornecidos."

    # Formatação das recomendações e geração das mensagens
    formatted_recommendations = [format_movie(movie) for _, movie in recommendations.iterrows()]
    recommendation_messages = []
    if title or genres or description:
        base_movie = df[df['Series_Title'].str.contains(title, case=False, na=False)] if title else None
        if base_movie is not None and not base_movie.empty:
            base_movie = base_movie.iloc[0:1]  # Pega apenas a primeira linha como referência
        recommendation_messages = [
            generate_recommendation_message(base_movie, movie, title, genres, description)
            for _, movie in recommendations.iterrows()
        ]

    # Incluindo todos os parâmetros na resposta
    return {
        "title": title if title else "Não fornecido",
        "genres": genres if genres else "Não fornecido",
        "description": description if description else "Não fornecido",
        "recommendations": formatted_recommendations,
        "messages": recommendation_messages if recommendation_messages else [generic_message]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
