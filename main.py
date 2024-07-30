import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from googletrans import Translator
from model import df, recommend_movies
from utils import format_movie, generate_recommendation_message

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
    
    translation = translator.translate(query, src='pt', dest='en')
    translated_query = translation.text
    
    results = df[df['Series_Title'].str.contains(translated_query, case=False, na=False)]
    if results.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": query})
    
    formatted_results = [format_movie(movie) for _, movie in results.iterrows()]
    return templates.TemplateResponse("search_results.html", {"request": request, "results": formatted_results})

@app.get("/recommendados/")
def recommend_movies_endpoint(request: Request, title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Title parameter is required")
    
    translation = translator.translate(title, src='pt', dest='en')
    translated_title = translation.text
    
    base_movie = df[df['Series_Title'].str.contains(translated_title, case=False, na=False)]
    if base_movie.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": title})
    
    base_movie = base_movie.iloc[0]
    recommendations = recommend_movies(translated_title)
    if recommendations is None or recommendations.empty:
        return templates.TemplateResponse("not_found.html", {"request": request, "query": title})
    
    formatted_recommendations = [format_movie(movie) for _, movie in recommendations.iterrows()]
    recommendation_messages = [generate_recommendation_message(base_movie, movie) for _, movie in recommendations.iterrows()]
    
    return templates.TemplateResponse(
        "recommendations.html",
        {
            "request": request,
            "title": title,
            "recommendations": formatted_recommendations,
            "recommendation_messages": recommendation_messages,
            "message": f"Esses filmes foram recomendados a partir da busca de '{title}' pois se assemelham nos quesitos gênero e avaliações.",
            "zip": zip  # Passar a função zip para o contexto do template
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
