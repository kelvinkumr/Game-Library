"""Initialize Flask app."""
from pathlib import Path

from flask import Flask, render_template
import games.adapters.repository as repo

from games.adapters import database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables

from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository
from flask import Flask, render_template, redirect, url_for, request
from games.authentication.authentication import login_required
from flask import session
import games.authentication.services as auth_services

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    app.secret_key = 'your_secret_key_here'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()


    # Build the application - these steps require an application context.
    with app.app_context():
        from .reviews import reviews
        app.register_blueprint(reviews.reviews_blueprint)
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        from .genres import genres
        app.register_blueprint(genres.genres_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    @app.route('/')
    def home():
        return render_template('home.html', title="Home")

    @app.route('/game/<int:game_id>')
    def gameDescription(game_id):
        game = repo.repo_instance.get_game_by_id(game_id)

        if game is None:
            return "Game not found", 404

        return redirect(url_for('view_game', id=game_id))

    @app.route('/search')
    def search():
        query = request.args.get('query', '').strip()
        if query:
            search_results = repo.repo_instance.search_games(query)
            return render_template('search.html', query=query, results=search_results)
        else:
            return redirect(url_for('home'))

    @app.route('/profile/<username>')
    @login_required
    def user_profile(username):
            # Obtain the user name of the currently logged in user
        name = session['user_name']

        try:
            #check if user has a valid session, if not return to login page
            auth_services.get_user(name, repo.repo_instance)

        except auth_services.UnknownUserException:
            return redirect(url_for('authentication_bp.login'))

        user = repo.repo_instance.get_user(name)
        wishlist = repo.repo_instance.get_wishlist_games(user)
        return render_template('profile.html', username=username,
                               user=repo.repo_instance.get_user(username),
                               reviews=repo.repo_instance.get_reviews(repo.repo_instance.get_user(username)),
                               wishlist=wishlist, num_games=repo.repo_instance.get_number_of_wishlist_games(user))

    @app.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
    @login_required
    def add_game_to_wishlist(game_id):
        repo.repo_instance.add_wishlist_game(repo.repo_instance.get_game_by_id(game_id),
                                             repo.repo_instance.get_user(session.get('user_name')))
        return redirect(url_for('gameDescription', game_id=game_id))

    @app.route('/remove_from_wishlist/<int:game_id>', methods=['POST'])
    @login_required
    def remove_from_wishlist(game_id):
        repo.repo_instance.remove_wishlist_game(repo.repo_instance.get_game_by_id(game_id),
                                                repo.repo_instance.get_user(session.get('user_name')))
        return redirect(url_for('gameDescription', game_id=game_id))

    return app