from datetime import date, datetime

import pytest
from sqlalchemy import inspect

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, make_comment
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repository = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repository.add_user(user)

    repository.add_user(User('Martin', '123456789'))

    user2 = repository.get_user('Dave')

    assert user2 is user
