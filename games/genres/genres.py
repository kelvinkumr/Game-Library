from flask import Flask, render_template, Blueprint
from games.genres import services
from games.adapters.repository import AbstractRepository
import games.adapters.repository as repo

genres_blueprint = Blueprint('genres_bp', __name__)


@genres_blueprint.route('/genres/<genre>/<int:page>', methods=['GET'])
def browse_genre(genre, page):
    if page <= 1:
        page = 1
    num_games = services.get_number_of_games_of_type(repo.repo_instance, genre)
    all_games = services.get_games_of_type(repo.repo_instance, genre, page)
    sorted_games = sorted(all_games, key=lambda game: game.title)
    return render_template('gameLibrary.html', title=genre, games=sorted_games, num_games=num_games, index=page,
                           pagePath='genres_bp.browse_genre', genre=genre)
