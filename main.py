from fastapi import FastAPI
from model import df
from utils import format_movie

app = FastAPI()


@app.get("/")
def home():
    return "Minha APi esta funcionando"

@app.get("/busca/")
def search_movies(query: str):
    results = df[df['Title'].str.contains(query, case=False, na=False)]
    formatted_results = [format_movie(movie) for _, movie in results.iterrows()]
    return formatted_results

@app.get("/recomendados/")
def recommend_movies(title: str):
    movie = df[df['Title'].str.contains(title, case=False, na=False)].iloc[0]
    cluster = movie['Cluster']
    
    recommendations = df[df['Cluster'] == cluster].sample(5)
    formatted_recommendations = [format_movie(movie) for _, movie in recommendations.iterrows()]
    return formatted_recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
