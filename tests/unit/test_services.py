import pytest

from games.domainmodel.model import Publisher, Genre, Game, User, Review, Wishlist
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from games.browse import services as games_services
from games.genres import services as genre_services
from games.wishlist import services as wishlist_services
from games.reviews import services as reviews_services


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(repo, "../../tests/data/test_games.csv")
    return repo


# Tests to see if the correct number of games is shown.
def test_get_num_total_games(in_memory_repo):
    total_games = games_services.get_number_of_games(in_memory_repo)
    assert total_games == 99


# Tests to see if each full page returns 20 games for pagination.
def test_get_num_games_per_page(in_memory_repo):
    page_num = 1

    # Goes through each page and checks if there are the correct number of games in that page.
    while page_num <= 5:
        games = games_services.get_games(in_memory_repo, page_num)

        if page_num == 5:
            # Since there are 99 games in the test file, the last page will have 15 games.
            assert len(games) == 15
        else:
            # Every page should normally return 21 games unless it is the last page.
            assert len(games) == 21
        page_num += 1


# Similar to above, but is genre-specific.
def test_get_num_genre_games_per_page(in_memory_repo):
    page_num = 1

    # Goes through each page and checks if there are the correct number of games in that page.
    while page_num <= 4:
        games = genre_services.get_games_of_type(in_memory_repo, "Indie", page_num)

        if page_num == 4:
            # Since there are 64 games in the test file with Indie as the genre, the last page will have 1 game.
            assert len(games) == 1
        else:
            # Every page should normally return 21 games unless it is the last page.
            assert len(games) == 21
        page_num += 1


def test_get_number_of_genre_games(in_memory_repo):
    num_games = genre_services.get_number_of_games_of_type(in_memory_repo, "Indie")
    assert num_games == 64
    num_games = genre_services.get_number_of_games_of_type(in_memory_repo, "Action")
    assert num_games == 99
    num_games = genre_services.get_number_of_games_of_type(in_memory_repo, "Adventure")
    assert num_games == 82


def test_search_for_game_by_name_functionality(in_memory_repo):
    games = in_memory_repo.search_games("super")
    assert games[0] == Game(572510, "Superola Champion Edition")


# If the search does not yield any results, it should return an empty list
def test_unavailable_search_for_game_by_name_functionality(in_memory_repo):
    games = in_memory_repo.search_games("sadasdwqdAS")
    # Returns an empty list.
    assert games == list()
    # List has no size.
    assert len(games) == 0

# If the search is not a string, it returns an empty list
def test_invalid_search_for_game_by_name_functionality(in_memory_repo):
    games = in_memory_repo.search_games("1234")
    # Returns an empty list.
    assert games == list()


def test_repository_can_add_to_wishlist(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)

    assert a_game in in_memory_repo.get_wishlist_games(a_user)


def test_repository_can_get_num_of_wishlist_games(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 0

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 1

    a_game = in_memory_repo.get_game_by_id(465070)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 2

    a_game = in_memory_repo.get_game_by_id(1581010)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 3


# Tests to see if each full wishlist page returns 20 games for pagination.
def test_get_num_wishlist_games_per_page(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    games = in_memory_repo.get_games()

    # Adds all games to the wishlist as a test.
    for i in range(len(games)):
        a_user.add_favourite_game(Game(games[i].game_id, games[i].title))

    page_num = 1

    # Goes through each wishlist page. Each page should return 9 games due to pagination.
    while page_num <= 11:
        game_count = len(wishlist_services.get_wishlist_games(in_memory_repo, page_num, a_user))
        page_num += 1
        assert game_count == 9


def test_repository_can_add_to_wishlist(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)

    assert a_game in in_memory_repo.get_wishlist_games(a_user)


def test_repository_can_get_num_of_wishlist_games(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 0

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 1

    a_game = in_memory_repo.get_game_by_id(465070)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 2

    a_game = in_memory_repo.get_game_by_id(1581010)
    in_memory_repo.add_wishlist_game(a_game, a_user)
    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 3


# Tests to see if each full wishlist page returns 9 games for pagination.
def test_get_num_wishlist_games_per_page(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    games = in_memory_repo.get_games()

    # Adds all games to the wishlist as a test.
    for i in range(len(games)):
        a_user.add_favourite_game(Game(games[i].game_id, games[i].title))


    page_num = 1

    # Goes through each wishlist page. Each page should return 9 games due to pagination.
    while page_num <= 11:
        game_count = len(wishlist_services.get_wishlist_games(in_memory_repo, page_num, a_user))
        page_num += 1
        assert game_count == 9


def test_add_review(in_memory_repo):
    # Creates a user and adds the user to the repo.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    a_game = in_memory_repo.get_game_by_id(267360)

    a_review = Review(a_user, a_game, 5, "Generic comment")
    a_user.add_review(a_review)

    # Checks to see if the review has been added.
    assert len(a_user.reviews) == 1










