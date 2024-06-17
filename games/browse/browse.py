from flask import Flask, render_template, Blueprint
from games.browse import services
from games.adapters.repository import AbstractRepository
import games.adapters.repository as repo


browse_blueprint = Blueprint('games_bp', __name__)

@browse_blueprint.route('/library/<int:page>', methods=['GET'])
def browse_games(page):
    if page <= 1:
        page = 1
    num_games = services.get_number_of_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance, page)
    return render_template('gameLibrary.html', title='Games Library', games=all_games, num_games=num_games, index = page, pagePath = 'games_bp.browse_games', genre=None)