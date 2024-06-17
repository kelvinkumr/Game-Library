from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

game_genres_table = Table('game_genres', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('game_id', ForeignKey('games.game_id')),
                          Column('genre_name', ForeignKey('genres.genre_name')),
                          )

users_table = Table('users', metadata,
                    Column('user_id', Integer, primary_key=True, autoincrement=True),
                    Column('username', String(64), nullable=False),
                    Column('password', String(64), nullable=False)
                    )

wishlist_table = Table('wishlist', metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('user_id', ForeignKey('users.user_id')),
                       Column('game_id', ForeignKey('games.game_id'))
                       )

reviews_table = Table('reviews', metadata,
                      Column('review_id', Integer, primary_key=True, autoincrement=True),
                      Column('game_id', Integer, ForeignKey('games.game_id')),
                      Column('rating', Integer, nullable=False),
                      Column('comment', String(64), nullable=True),
                      Column('user_id', ForeignKey('users.user_id'))
                      )

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review),
        '_User__wishlist': relationship(Wishlist)
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__reviews': relationship(Review)
    })

    mapper(Review, reviews_table, properties={
        '_Review__rating': reviews_table.c.rating,
        '_Review__comment': reviews_table.c.comment,
        '_Review__game_id': reviews_table.c.game_id,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })

    mapper(Wishlist, wishlist_table, properties={
        '_Wishlist__user': relationship(User, back_populates='_User__wishlist'),
        '_Wishlist__game_id': relationship(Game)
    })
