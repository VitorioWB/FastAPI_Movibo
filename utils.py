def format_movie(movie):
    return {
        "Title": movie["Title"],
        "Genre": movie["Genre"],
        "Director": movie["Director"],
        "IMDB_Rating": movie["IMDB_Rating"],
        "Meta_score": movie["Meta_score"],
        "Description": movie["Description"]
    }
