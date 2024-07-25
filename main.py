from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from model import df
from utils import format_movie

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/busca/")
def search_movies(request: Request, query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    results = df[df['Series_Title'].str.contains(query, case=False, na=False)]
    
    if results.empty:
        raise HTTPException(status_code=404, detail="No movies found with the given query")
    
    formatted_results = [format_movie(movie) for _, movie in results.iterrows()]
    return templates.TemplateResponse("search_results.html", {"request": request, "results": formatted_results})

@app.get("/recommendados/")
def recommend_movies(request: Request, title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Title parameter is required")
    
    results = df[df['Series_Title'].str.contains(title, case=False, na=False)]
    if results.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie = results.iloc[0]
    cluster = movie['Cluster']
    recommendations = df[df['Cluster'] == cluster].sample(5)
    formatted_recommendations = [format_movie(movie) for _, movie in recommendations.iterrows()]
    return templates.TemplateResponse("recommendations.html", {"request": request, "title": title, "recommendations": formatted_recommendations})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
