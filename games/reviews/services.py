from typing import List, Iterable

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import make_comment, Game


class NonExistentGameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(game_id: int, comment_text: str, user_name: str, rating: int, repository_mode: str, repo: AbstractRepository):
    # Check that the game exists.
    game = repo.get_game_by_id(game_id)
    if game is None:
        raise NonExistentGameException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    review = make_comment(comment_text, user, rating, game, repository_mode)

    # Update the repository.
    repo.add_review(review)

def get_game(game_id: int, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)
    if game is None:
        raise NonExistentGameException
    
    return game

