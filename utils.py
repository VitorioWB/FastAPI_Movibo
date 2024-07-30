from googletrans import Translator

translator = Translator()

def format_movie(movie):
    description_translation = translator.translate(movie["Overview"], src='en', dest='pt')
    translated_description = description_translation.text
    return {
        "Title": movie["Series_Title"],
        "Genre": movie["Genre"],
        "Director": movie["Director"],
        "IMDB_Rating": movie["IMDB_Rating"],
        "Meta_score": movie["Meta_score"],
        "Description": translated_description,
        "Poster_Link": movie["Poster_Link"]
    }

def generate_recommendation_message(base_movie, recommended_movie):
    base_genres = set(base_movie["Genre"].split(", "))
    recommended_genres = set(recommended_movie["Genre"].split(", "))
    common_genres = base_genres.intersection(recommended_genres)

    message = f"O filme '{recommended_movie['Series_Title']}' foi recomendado pois "

    if common_genres:
        message += f"apresenta os gêneros {', '.join(common_genres)}"
    else:
        message += "é popular e bem avaliado."

    return message
