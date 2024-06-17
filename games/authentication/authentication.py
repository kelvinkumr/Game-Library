from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
import games.authentication.services as services
import games.adapters.repository as repo

# Makes the Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        # A successful POST request, meaning that the provided username and password have been validated.
        # We will now utilize the service layer to try adding the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)

            # Everything is in order, so guide the user to the login page for further action.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your user name is already taken - please supply another'

    # In the case of a GET request or an unsuccessful POST request, provide the Registration Web page as the response.
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register'),
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        # Following a successful POST request, where the username and password have passed validation,
        # utilize the service layer to search for the user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            # Authenticate the user
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            # Initialize a session and guide the user to the homepage through a redirection.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            # If the username is not recognized by the system, assign an appropriate error message.
            user_name_not_recognised = 'User name not recognised - please supply another'
        except services.AuthenticationException:
            # If authentication fails, assign an appropriate error message.
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'
    # In the case of a GET request or an unsuccessful POST request, provide the Login Web page as the response.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')