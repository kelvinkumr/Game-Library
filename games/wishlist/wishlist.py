from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm

import games.adapters.repository as repo
import games.wishlist.services as services
import games.authentication.services as auth_services

from games.authentication.authentication import login_required

# Configure Blueprint.
wishlist_blueprint = Blueprint(
    'wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist/<name>/<int:page>', methods=['GET', 'POST'])
@login_required
def view_wishlist(name, page):
    if page <= 1:
        page = 1

    try:
        # check if user has a valid session, if not return to login page
        auth_services.get_user(name, repo.repo_instance)
    except auth_services.UnknownUserException:
        return redirect(url_for('authentication_bp.login'))

    num_games = services.get_number_of_wishlist_games(repo.repo_instance, repo.repo_instance.get_user(session.get('user_name')))
    all_games = services.get_wishlist_games(repo.repo_instance, page, repo.repo_instance.get_user(session.get('user_name')))

    return render_template(
        'wishlist.html',
        name=name,
        games=all_games,
        num_games=num_games,
        index=page,
        genre=None,
        pagePath='wishlist_bp.view_wishlist'
    )

