from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
from games.domainmodel.model import Genre


def get_number_of_games_of_type(repo: AbstractRepository, genre: str):
    games_length = repo.get_number_of_games_of_type(genre)
    return games_length


def get_games_of_type(repo: AbstractRepository, genre: str, page):
    games = repo.get_games()
    games_list = []
    genre_to_find = Genre(genre)
    amount_per_page = 21
    for game in games:
        list_of_genres = game.genres
        for genre_in_list in list_of_genres:
            if genre_to_find == genre_in_list:
                games_list.append(game)
    if amount_per_page * page > len(games_list):
        return games_list[
               amount_per_page * (page - 1): amount_per_page * page - (amount_per_page * page - len(games_list))]
    else:
        return games_list[amount_per_page * (page - 1): amount_per_page * page]
