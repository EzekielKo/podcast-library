"""Initialize Flask app."""


from flask import Flask
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers, registry
from sqlalchemy.pool import NullPool

from podcast.adapters.memoryRepository import MemoryRepository, populate
from podcast.adapters.orm import metadata, map_model_to_tables
from podcast.catalogue.catalogue import create_catalogue_blueprint
from podcast.description.description import create_podcast_description_blueprint
from podcast.search.search import create_podcast_search_blueprint

from podcast.authentication.authentication import create_authentication_blueprint
from podcast.playlist.playlist import create_playlist_blueprint
from podcast.home.home import create_home_blueprint

from podcast.adapters.databaseRepository import SqlAlchemyRepository, populate_database


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('podcast') / 'adapters' / 'data'


    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Use the passed repo_instance if provided, otherwise create a new one.

    repo_instance = MemoryRepository()
    populate(repo_instance, data_path)

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo_instance = MemoryRepository()
        if repo_instance:
            print('using memory')
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        # database_mode = False
        populate(repo_instance, data_path)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']


        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo_instance = SqlAlchemyRepository(session_factory)
        if repo_instance:
            print("using database")

        inspector = inspect(database_engine)
        tables = inspector.get_table_names()

        if app.config['TESTING'] == 'True':
            print("TESTING MODE: REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)

            with database_engine.connect() as connection:
                trans = connection.begin()
                try:
                    for table in reversed(metadata.sorted_tables):
                        connection.execute(table.delete())
                    trans.commit()
                except:
                    trans.rollback()
                    raise

            map_model_to_tables()
            populate_database(repo_instance, data_path)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            if not tables:
                print("FIRST-TIME SETUP: CREATING TABLES AND POPULATING DATABASE...")
                clear_mappers()
                metadata.create_all(database_engine)

                map_model_to_tables()
                populate_database(repo_instance, data_path)
                print("FIRST-TIME SETUP... FINISHED")
            else:
                map_model_to_tables()

    with app.app_context():
        # Register blueprints with the repository instance.
        app.register_blueprint(create_home_blueprint(repo_instance))
        app.register_blueprint(create_catalogue_blueprint(repo_instance))
        app.register_blueprint(create_podcast_description_blueprint(repo_instance))
        app.register_blueprint(create_podcast_search_blueprint(repo_instance))
        app.register_blueprint(create_authentication_blueprint(repo_instance))
        app.register_blueprint(create_playlist_blueprint(repo_instance))

    return app
