from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import games.adapters.repository as repo
import games.reviews.services as services
import games.authentication.services as auth_services

from dotenv import load_dotenv
import os

from games.authentication.authentication import login_required

# Load environment variables from the .env file
load_dotenv()

repository_mode = os.getenv('REPOSITORY')

# Configure Blueprint.
reviews_blueprint = Blueprint(
    'reviews_bp', __name__)

@reviews_blueprint.route('/game/<int:game_id>')
def gameDescription(game_id):
    game = repo.repo_instance.get_game_by_id(game_id)
    form=CommentForm(request.values, game_id = game_id)

    return render_template('gameDescription.html', form=form, game=game, add_comment_url = '/comment', handler_url=url_for('reviews_bp.comment_on_game'))

@reviews_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_game():
    # Obtain the user name of the currently logged in user
    user_name = session['user_name']

    try:
        #check if user has a valid session, if not return to login page
        auth_services.get_user(user_name, repo.repo_instance)

    except auth_services.UnknownUserException:
        return redirect(url_for('authentication_bp.login'))
    
    # Create form, form gets populated when a POST method is entered from a form.
    form = CommentForm(request.form)

    if form.validate_on_submit():
        # Successful POST, form has valid input data
        game_id = int(form.game_id.data)
        cur_rating = request.form['rating']

        # Use the service layer to store the new review
        services.add_review(game_id, form.comment.data, user_name, cur_rating, repository_mode, repo.repo_instance)

        # Retrieve the game
        game = services.get_game(game_id, repo.repo_instance)

        # display all reviews, including the new review.
        return redirect(url_for('gameDescription', game_id = game_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the game id, representing the game to comment, from a query parameter of the GET request.
        game_id = int(request.args.get('game'))

        # Store the game id in the form.
        form.game_id.data = game_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the game id of the game being commented from the form.
        game_id = int(form.game_id.data)

    # unsucessful GET or POST.
    game = services.get_game(game_id, repo.repo_instance)

    return render_template(
        'reviews/commentOnGame.html',
        game=game,
        form=form,
        handler_url=url_for('reviews_bp.comment_on_game')
    )

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
    DataRequired(),
    Length(min=4, message='Your comment is too short')])
    game_id = HiddenField("Game id")
    current_rating = HiddenField("Rating", default=5)
    submit = SubmitField('Submit')