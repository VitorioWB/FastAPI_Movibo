def format_movie(movie):
    return {
        "Title": movie["Series_Title"],
        "Genre": movie["Genre"],
        "Director": movie["Director"],
        "IMDB_Rating": movie["IMDB_Rating"],
        "Meta_score": movie["Meta_score"],
        "Description": movie["Overview"],  # Mantemos a descrição original
        "Poster_Link": movie["Poster_Link"]
    }

def generate_recommendation_message(base_movie, recommended_movie, title=None, genres=None, description=None):
    messages = []

    # Garantir que base_movie não seja None e tenha a coluna 'Genre'
    if base_movie is not None and not base_movie.empty and "Genre" in base_movie:
        base_genres = set(base_movie["Genre"].iloc[0].split(", "))
    else:
        base_genres = set()
    
    recommended_genres = set(recommended_movie["Genre"].split(", "))
    common_genres = base_genres.intersection(recommended_genres)

    if title:
        messages.append(f"Foi recomendado com base no título '{title}' que você forneceu.")
    
    if genres:
        if common_genres:
            messages.append(f"Possui gêneros em comum: {', '.join(common_genres)}.")
        else:
            messages.append(f"Pertence a gêneros similares aos que você forneceu: {genres}.")
    
    if description:
        messages.append(f"A descrição possui termos semelhantes à frase '{description}' que você mencionou.")

    return " ".join(messages) if messages else "Recomendado com base nos critérios fornecidos."



