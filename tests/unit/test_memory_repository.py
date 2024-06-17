import pytest

from games.adapters.repository import RepositoryException
from games.domainmodel.model import Game, User, Review
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from tests.unit.test_domainmodel import user


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(repo, "../../tests/data/test_games.csv")
    return repo


def test_repository_can_add_a_game(in_memory_repo):
    game = Game(12121212, 'test_game_title')
    in_memory_repo.add_game(game)

    assert in_memory_repo.get_game_by_id(12121212) is game


def test_repository_can_get_num_games(in_memory_repo):
    num_games = in_memory_repo.get_number_of_games()
    assert num_games == 99


def test_repository_get_game_by_game_id_returns_game(in_memory_repo):
    assert isinstance(in_memory_repo.get_game_by_id(471770), Game)


def test_repository_can_get_game_by_game_id(in_memory_repo):
    assert in_memory_repo.get_game_by_id(471770)


def test_repository_increments_count(in_memory_repo):
    game = Game(1234567, 'test_game_title!')
    in_memory_repo.add_game(game)

    # Number of games should have increased from 99 to 100.
    num_games = in_memory_repo.get_number_of_games()
    assert num_games == 100


def test_repository_can_get_num_games_by_genre(in_memory_repo):
    num_games_genre = in_memory_repo.get_number_of_games_of_type("Indie")
    assert num_games_genre == 64


def test_repository_can_search_for_game(in_memory_repo):
    games = in_memory_repo.search_games("super")
    assert games[0] == Game(572510, "Superola Champion Edition")


def test_repository_gets_correct_amount_of_genre_games(in_memory_repo):
    indie_games = in_memory_repo.get_number_of_games_of_type("Indie")
    action_games = in_memory_repo.get_number_of_games_of_type("Action")
    adventure_games = in_memory_repo.get_number_of_games_of_type("Adventure")
    assert indie_games == 64
    assert action_games == 99
    assert adventure_games == 82


def test_repository_adds_user(in_memory_repo):
    a_user = User("username", "password")
    in_memory_repo.add_user(a_user)
    assert in_memory_repo.get_user('username') is a_user


def test_repository_can_get_a_user(in_memory_repo):
    a_user = User("username", "password")
    in_memory_repo.add_user(a_user)
    user = in_memory_repo.get_user('username')
    assert user == User('username', 'password')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('Vitali Volkov :-)')
    assert user is None


def test_repository_adds_review(in_memory_repo):
    # Creates a user and a game to add to review.
    a_user = User("george", "aPassword1")
    print(isinstance(a_user, User))
    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_user(a_user)

    a_review = Review(a_user, a_game, 4, "Good Game :-)")
    a_user.add_review(a_review)
    a_game.add_review(a_review)
    print(a_review.user)
    print(a_user.reviews)
    in_memory_repo.add_review(a_review)

    assert a_review in in_memory_repo.get_reviews(a_user)


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    # Adds a game to the repository.
    a_game = in_memory_repo.get_game_by_id(311120)

    try:
        # Exception expected because the review doesn't refer to a user.
        a_review = Review(None, a_game, 3, "Trump's onto it!")
        in_memory_repo.add_review(a_review)
    except ValueError:
        # Catch the ValueError and mark the test as passed
        pass

    else:
        # If no ValueError is raised, fail the test
        pytest.fail("Expected a ValueError but nothing was raised")


def test_repository_does_not_add_a_review_without_a_game_properly_attached(in_memory_repo):
    # Adds a game to the repository.
    a_user = User("Brad", "aPassword1")
    try:
        in_memory_repo.add_user(a_user)
        a_review = Review(a_user, None, 3, "Trump's onto it!")
    except ValueError:
        pass

    else:
        # If no ValueError is raised, fail the test
        pytest.fail("Expected a ValueError but nothing was raised")

    with pytest.raises(AttributeError):
        user.add_review(a_review)
        # Exception expected because the review doesn't refer to the game.
        in_memory_repo.add_review(a_review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    # Creates a user and 2 games
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)
    a_game1 = in_memory_repo.get_game_by_id(311120)
    a_game2 = in_memory_repo.get_game_by_id(465070)

    # Creates 2 reviews and adds them to repo.
    user = in_memory_repo.get_user("vitali")
    review1 = Review(user, a_game1, 1, "Test comment :-)")
    review2 = Review(user, a_game2, 2, "Test comment 2 :-)")
    user.add_review(review1)
    user.add_review(review2)
    a_game1.add_review(review1)
    a_game2.add_review(review2)
    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)

    assert len(in_memory_repo.get_reviews(a_user)) == 2


def test_repository_can_add_to_wishlist(in_memory_repo):
    # Creates a user.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)

    assert a_game in in_memory_repo.get_wishlist_games(a_user)


def test_repository_can_get_num_of_wishlist_games(in_memory_repo):
    # Creates a user.
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


def test_repository_can_remove_wishlist_games(in_memory_repo):
    # Creates a user.
    a_user = User("vitali", "aPassword1")
    in_memory_repo.add_user(a_user)

    a_game = in_memory_repo.get_game_by_id(311120)
    in_memory_repo.add_wishlist_game(a_game, a_user)

    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 1

    in_memory_repo.remove_wishlist_game(a_game, a_user)

    assert in_memory_repo.get_number_of_wishlist_games(a_user) == 0
