from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository, page):
    games = repo.get_games()
    game_dicts = []
    amount_per_page = 21

    for game in games:
        game_dict = {'game_id': game.game_id, 'title': game.title, 'release_date': game.release_date, 'image_url': game.image_url, 'price': game.price}
        game_dicts.append(game_dict)
    if amount_per_page*page > len(game_dicts):
        return game_dicts[amount_per_page*(page-1): amount_per_page*page - (amount_per_page*page - len(game_dicts))]
    else:
        return game_dicts[amount_per_page*(page-1): amount_per_page*page]