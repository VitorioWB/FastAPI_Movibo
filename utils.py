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
