from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from googletrans import Translator
from model import df
from utils import format_movie

app = FastAPI()
translator = Translator()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/busca/")
def search_movies(request: Request, query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    # Traduzir o termo de busca do português para o inglês
    translation = translator.translate(query, src='pt', dest='en')
    translated_query = translation.text
    print(f"Termo de busca traduzido: {translated_query}")
    
    results = df[df['Series_Title'].str.contains(translated_query, case=False, na=False)]
    
    if results.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": query})
    
    formatted_results = [format_movie(movie) for _, movie in results.iterrows()]
    return templates.TemplateResponse("search_results.html", {"request": request, "results": formatted_results})

@app.get("/recommendados/")
def recommend_movies(request: Request, title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Title parameter is required")
    
    # Traduzir o título do filme do português para o inglês
    translation = translator.translate(title, src='pt', dest='en')
    translated_title = translation.text
    print(f"Título traduzido: {translated_title}")
    
    results = df[df['Series_Title'].str.contains(translated_title, case=False, na=False)]
    if results.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": title})
    
    movie = results.iloc[0]
    cluster = movie['Cluster']
    genre = movie['Genre']
    director = movie['Director']
    print(f"Cluster do filme: {cluster}, Gênero: {genre}, Diretor: {director}")
    
    # Recomendar filmes do mesmo cluster, gênero e diretor
    recommendations = df[
        (df['Cluster'] == cluster) &
        (df['Genre'].str.contains(genre.split(',')[0], case=False, na=False)) &
        (df['Director'] == director)
    ]
    
    # Se não houver recomendações suficientes, relaxe os critérios
    if len(recommendations) < 5:
        recommendations = df[df['Cluster'] == cluster]
    
    print(f"Recomendações encontradas: {recommendations}")
    
    if recommendations.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": title})
    
    sample_recommendations = recommendations.sample(min(5, len(recommendations)))
    formatted_recommendations = [format_movie(movie) for _, movie in sample_recommendations.iterrows()]
    print(f"Recomendações formatadas: {formatted_recommendations}")
    
    return templates.TemplateResponse(
        "recommendations.html",
        {
            "request": request,
            "title": title,
            "recommendations": formatted_recommendations,
            "message": f"Esses filmes foram recomendados a partir da busca de '{title}' pois se assemelham nos quesitos gênero, diretor e cluster."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
