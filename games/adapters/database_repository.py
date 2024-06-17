from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from games.domainmodel.model import User, Game, Review, Genre, Publisher, Wishlist
from games.adapters.repository import AbstractRepository
from flask import request, render_template, redirect, url_for, session


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_game_by_id(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def get_number_of_games(self):
        number_of_games = self._session_cm.session.query(Game).count()
        return number_of_games

    def get_first_game(self):
        game = self._session_cm.session.query(Game).first()
        return game

    def get_last_game(self):
        game = self._session_cm.session.query(Game).order_by(desc(Game._game__id)).first()
        return game

    def get_games(self):
        games = self._session_cm.session.query(Game).all()
        return games

    def get_games_of_type(self, genre: Genre):
        games = self._session_cm.session.query(Game).join(Game._Game__genres).filter(Genre._Genre__genre_name == genre).all()
        return games

    def get_number_of_games_of_type(self, genre: Genre):
        num_games = self._session_cm.session.query(Game).join(Game._Game__genres).filter(Genre._Genre__genre_name == genre).count()
        return num_games

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    def get_reviews(self, user_name) -> List[Review]:
        comments = self._session_cm.session.query(Review).all()
        return comments

    def get_wishlist_games(self, user: User) -> List[Game]:
        wishlist_games = self._session_cm.session.query(Wishlist).filter_by(_Wishlist__user=user).all()
        game_objects = [self.get_game_by_id(game.game_id) for game in wishlist_games]
        return game_objects

    def get_number_of_wishlist_games(self, user: User) -> List[Game]:
        num_games = self._session_cm.session.query(Wishlist).filter_by(_Wishlist__user=user).count()
        return num_games

    # region Review_data

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.merge(review)
            scm.commit()

    def add_multiple_reviews(self, reviews: List[Review]):
        with self._session_cm as scm:
            for review in reviews:
                scm.session.merge(review)
            scm.commit()

    # endregion

    def add_wishlist_game(self, game: Game, user: User):
        wishlist = Wishlist(user)
        wishlist._Wishlist__game_id = game

        with self._session_cm as scm:
            scm.session.merge(wishlist)
            scm.commit()

    def remove_wishlist_game(self, game: Game, user: User):
        with self._session_cm as scm:
            # Retrieve the wishlist item based on the provided game and user
            wishlist_item = scm.session.query(Wishlist).filter_by(_Wishlist__user=user, _Wishlist__game_id=game).first()
            # Check if the wishlist item exists before trying to remove it
            if wishlist_item:
                scm.session.delete(wishlist_item)  # Remove the wishlist item from the session
                scm.commit()  # Commit the changes to the database

    def search_games(self, query):

        search = "%{}%".format(query)

        genre_count = self._session_cm.session.query(Game).join(Game._Game__genres).filter(
            Genre._Genre__genre_name.like(search)).count()

        # Searches for games of type genre.
        genre_games = self._session_cm.session.query(Game).join(Game._Game__genres).filter(
            Genre._Genre__genre_name.like(search)).all()
        game_objects = [self.get_game_by_id(game.game_id) for game in genre_games]

        # Searches for games with title.
        if genre_count == 0:
            selected_games = self._session_cm.session.query(Game).filter(Game._Game__game_title.like(search)).all()
            game_objects = [self.get_game_by_id(game.game_id) for game in selected_games]

        return game_objects


