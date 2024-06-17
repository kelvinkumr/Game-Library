import abc
from typing import List
from games.domainmodel.model import Game, Publisher, Genre, Review, User, Wishlist

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        """ Add a game to repository list of games """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """Returns the list of games"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        """returns a number of games exist in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_of_type(self, genre: str):
        """returns all games of same genre type"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games_of_type(self, genre: str):
        """returns total number of games that exist with genre"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Game and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.game is None or review not in review.game.reviews:
            raise RepositoryException('Review not correctly attached to a Game')

    @abc.abstractmethod
    def get_number_of_wishlist_games(self, user: User):
        """returns a number of wishlist games in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_wishlist_games(self, user: User):
        """returns all wishlist games in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_wishlist_game(self, game: Game, user: User):
        """Adds a wishlist game to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_wishlist_game(self, game: Game, user: User):
        """Removes a wishlist game from the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_genres(self, genres: List[Genre]):
        """ Add many genres to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_games(self, games: List[Game]):
        """ Add multiple games to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_publishers(self, publisher: List[Publisher]):
        """ Add multiple publishers to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_reviews(self, review: List[Review]):
        """ Add multiple reviews to the repository of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, user_name) -> List[Review]:
        """ Returns all reviews """
        raise NotImplementedError

    @abc.abstractmethod
    def search_games(self, query) -> List[Game]:
        """ Returns all games with query """
        raise NotImplementedError
