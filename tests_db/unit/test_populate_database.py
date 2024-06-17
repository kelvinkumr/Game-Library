from sqlalchemy import select, inspect

from games.adapters.orm import metadata
from games.domainmodel.model import Game, User, Review
from games.adapters.database_repository import SqlAlchemyRepository
from tests_db.conftest import session_factory


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres',
                                           'publishers', 'reviews', "users", "wishlist"]


def test_database_populate_select_all_users(database_engine, session_factory):

    # Get table information
    inspector = inspect(database_engine)
    a_user1 = User("thorke", "Password1!")
    a_user2 = User("fmercury", "Password1!")

    repo = SqlAlchemyRepository(session_factory)

    name_of_users_table = inspector.get_table_names()[5]
    repo.add_user(a_user1)
    repo.add_user(a_user2)

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury']
