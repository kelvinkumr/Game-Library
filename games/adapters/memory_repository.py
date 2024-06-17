from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import Game, User, Review, Wishlist
from games.domainmodel.model import Genre
import os.path
import bisect


def calculate_similarity(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    dp = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    for i in range(len_str1 + 1):
        for j in range(len_str2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len_str1][len_str2]


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = list()
        self.__users = list()
        self.__reviews = list()
        self.__wishlist = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            bisect.insort_left(self.__games, game)

    def get_games(self) -> list[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_games_of_type(self, genre):
        return self.__games

    def get_number_of_games_of_type(self, genre):
        games_list = []
        genre_to_find = Genre(genre)
        for game in self.__games:
            for genre_current in game.genres:
                if genre_to_find == genre_current:
                    games_list.append(game)
        return len(games_list)

    def get_game_by_id(self, game_id):
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def search_games(self, query):
        query = query.lower()
        results = []
        exact_match = None
        substrings = []

        for game in self.__games:
            if query == game.title.lower():
                exact_match = game
            elif query in game.title.lower():
                substrings.append(game)
            else:
                similarity = calculate_similarity(query, game.title.lower())
                similarity_threshold = 3

                if similarity <= similarity_threshold:
                    results.append(game)

        substrings = sorted(substrings, key=lambda game: game.title)
        results = sorted(results, key=lambda game: game.title)
        results = substrings + results
        if exact_match is not None:
            results.insert(0, exact_match)
        return results

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

    def get_reviews(self, user: User):
        reviews = [x for x in self.__reviews if x.user == user]
        return reviews[::-1]

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_number_of_wishlist_games(self, user: User):
        """returns a number of wishlist games in the repository"""
        return len(user.favourite_games)

    def get_wishlist_games(self, user: User):
        """returns all wishlist games in the repository"""
        return user.favourite_games

    def add_wishlist_game(self, game: Game, user: User):
        """Adds a wishlist game to the repository"""
        if game not in user.favourite_games:
            user.add_favourite_game(game)

    def remove_wishlist_game(self, game: Game, user: User):
        """Removes a wishlist game from the repository"""
        if game in user.favourite_games:
            user.remove_favourite_game(game)


def populate(repo: AbstractRepository, csv_path="data/games.csv"):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, csv_path)
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)
