import requests
import os
from dotenv import load_dotenv
import pandas as pd

BASE_URL = "https://api.themoviedb.org/3"



def get_movies_df(num_page):
    HEADERS =  {"Authorization": f"Bearer TOKEN"}
    params = {
        "page": num_page,
        "sort_by": "popularity.desc",
        "vote_count.gte": 100
    }

    response = requests.get(
        f"{BASE_URL}/discover/movie",
        headers=HEADERS,
        params=params
    )

    data = response.json()
    df = pd.DataFrame(data["results"])

    return df[["id", "title", "release_date"]]

def get_movie_info_df(movie_id):
    HEADERS =  {"Authorization": f"Bearer TOKEN"}

    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}?append_to_response=credits",
        headers=HEADERS
    )

    data = response.json()

    movie_df = pd.DataFrame([{
        "movie_id": data.get("id"),
        "title": data.get("title"),
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime"),
        "budget": data.get("budget"),
        "revenue": data.get("revenue"),
        "vote_average": data.get("vote_average"),
        "vote_count": data.get("vote_count"),
        "popularity": data.get("popularity"),
        "original_language": data.get("original_language")
    }])

    cast = data.get("credits", {}).get("cast", [])[:5]

    actors_df = pd.DataFrame([
        {
            "actor_id": actor.get("id"),
            "name": actor.get("name")
        }
        for actor in cast
    ])


    movie_actor_df = pd.DataFrame([
        {
            "movie_id": movie_id,
            "actor_id": actor.get("id"),
            "order": actor.get("order")
        }
        for actor in cast
    ])

    genres = data.get("genres", [])

    genres_df = pd.DataFrame([
        {
            "genre_id": g.get("id"),
            "genre_name": g.get("name")
        }
        for g in genres
    ])


    movie_genre_df = pd.DataFrame([
        {
            "movie_id": movie_id,
            "genre_id": g.get("id")
        }
        for g in genres
    ])

    return movie_df, actors_df, movie_actor_df, genres_df, movie_genre_df


def get_actor_info(actor_id):
    HEADERS =  {"Authorization": f"Bearer TOKEN"}

    response = requests.get(
        f"{BASE_URL}/person/{actor_id}",
        headers=HEADERS
    )

    data = response.json()

    # -------- gênero --------
    gender_map = {
        0: "not_specified",
        1: "female",
        2: "male",
        3: "non_binary"
    }

    gender = gender_map.get(data.get("gender"), "unknown")

    # -------- morto --------
    deathday = data.get("deathday")
    dead = bool(deathday)

    # -------- dataframe --------
    df = pd.DataFrame([{
        "id": data.get("id"),
        "name": data.get("name"),
        "birthday": data.get("birthday"),
        "deathday": deathday,
        "dead": dead,
        "gender": gender,
        "popularity": data.get("popularity"),
        "known_for_department": data.get("known_for_department"),
        "place_of_birth": data.get("place_of_birth")
    }])

    return df
