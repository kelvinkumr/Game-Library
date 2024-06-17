from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User


def get_number_of_wishlist_games(repo: AbstractRepository, user: User):
    return repo.get_number_of_wishlist_games(user)


def get_wishlist_games(repo: AbstractRepository, page, user: User):
    games = repo.get_wishlist_games(user)
    game_dicts = []
    amount_per_page = 9

    for game in games:
        game_dict = {'game_id': game.game_id, 'title': game.title, 'game_url': game.release_date,
                     'image_url': game.image_url}
        game_dicts.append(game_dict)
    if amount_per_page * page > len(game_dicts):
        return game_dicts[
               amount_per_page * (page - 1): amount_per_page * page - (amount_per_page * page - len(game_dicts))]
    else:
        return game_dicts[amount_per_page * (page - 1): amount_per_page * page]
