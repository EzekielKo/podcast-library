from typing import List
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Podcast, Episode, Author, Category, Review, Playlist, User
from podcast.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # This method can be used e.g., to allow Flask to start a new session for each HTTP request,
        # via the 'before_request' callback.
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # Podcast methods
    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.add(podcast)
            scm.commit()

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            podcast = self._session_cm.session.query(Podcast).filter(Podcast._id == podcast_id).one()
        except NoResultFound:
            pass
        return podcast

    def get_all_podcasts(self) -> List[Podcast]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    # Episode methods
    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.add(episode)
            scm.commit()

    def get_episode(self, episode_id: int) -> Episode:
        episode = None
        try:
            episode = self._session_cm.session.query(Episode).filter(Episode._id == episode_id).one()
        except NoResultFound:
            pass
        return episode

    def add_episode_to_playlist(self, episode: Episode, playlist: Playlist):
        with self._session_cm as scm:
            playlist.add_episode(episode)
            scm.session.add(playlist)
            scm.commit()

    def remove_episode_from_playlist(self, episode: Episode, playlist: Playlist):
        with self._session_cm as scm:
            playlist.remove_episode(episode)
            scm.session.add(playlist)
            scm.commit()

    # Author methods
    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_author(self, author_id: int) -> Author:
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._id == author_id).one()
        except NoResultFound:
            pass
        return author

    # Category methods
    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.add(category)
            scm.commit()

    def get_category(self, category_id: int) -> Category:
        category = None
        try:
            category = self._session_cm.session.query(Category).filter(Category._id == category_id).one()
        except NoResultFound:
            pass
        return category

    def get_all_categories(self) -> List[Category]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    # Review methods
    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_review_to_podcast(self, review: Review, podcast: Podcast):
        with self._session_cm as scm:
            podcast.add_review(review)
            scm.session.add(podcast)
            scm.commit()

    def get_next_review_id(self) -> int:
        max_id = self._session_cm.session.query(func.max(Review._id)).scalar()
        return (max_id or 0) + 1

    def get_review(self, review_id: int) -> Review:
        review = None
        try:
            review = self._session_cm.session.query(Review).filter(Review._id == review_id).one()
        except NoResultFound:
            pass
        return review

    def get_reviews_for_podcast(self, podcast_id: int) -> List[Review]:
        reviews = self._session_cm.session.query(Review).filter(Review._podcast_id == podcast_id).all()
        return reviews

    # Playlist methods
    def add_playlist(self, playlist: Playlist):
        with self._session_cm as scm:
            scm.session.add(playlist)
            scm.commit()

    def get_playlist(self, playlist_id: int) -> Playlist:
        playlist = None
        try:
            playlist = self._session_cm.session.query(Playlist).filter(Playlist._id == playlist_id).one()
        except NoResultFound:
            pass
        return playlist

    def get_next_playlist_id(self) -> int:
        max_id = self._session_cm.session.query(func.max(Playlist._id)).scalar()
        return (max_id or 0) + 1

    def get_playlist_by_user(self, user: User) -> Playlist:
        playlist = None
        try:
            playlist = self._session_cm.session.query(Playlist).filter(Playlist._owner == user).one()
        except NoResultFound:
            pass
        return playlist

    # User methods
    def add_user(self, user: User):
        print("called add user")
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_id: int) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._id == user_id).one()
        except NoResultFound:
            pass
        return user

    def get_next_user_id(self) -> int:
        # Query to find the maximum ID in the users table
        max_id = self._session_cm.session.query(func.max(User._id)).scalar()
        # Return the next available ID, incrementing from the current max_id
        return (max_id or 0) + 1

    def get_user_by_username(self, username: str) -> User:
        print('called "get user by username"')
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._username == username).one()
        except NoResultFound:
            pass
        return user


def load_data(data_path, repo: SqlAlchemyRepository):
    # Initialize the CSVDataReader
    csv_reader = CSVDataReader(data_path)
    csv_reader.read_podcasts()
    csv_reader.read_episodes()

    with repo._session_cm as scm:
        # Add authors
        for author in csv_reader.authors:
            existing_author = scm.session.query(Author).filter_by(_id=author.id).first()
            if not existing_author:
                scm.session.add(author)
        scm.commit()

        # Add categories
        for category in csv_reader.categories:
            existing_category = scm.session.query(Category).filter_by(_id=category.id).first()
            if not existing_category:
                scm.session.add(category)
        scm.commit()

        # Add podcasts
        for podcast in csv_reader.podcasts:
            # Retrieve existing author from the session
            author = scm.session.query(Author).filter_by(_id=podcast.author.id).first()
            if author:
                podcast._author = author

            # Replace categories with those from the session
            categories = []
            for category in podcast.categories:
                cat = scm.session.query(Category).filter_by(_id=category.id).first()
                if cat:
                    categories.append(cat)
            podcast.categories = categories

            scm.session.add(podcast)
        scm.commit()

        # Add episodes
        for episode in csv_reader.episodes:
            # Retrieve existing podcast from the session
            podcast = scm.session.query(Podcast).filter_by(_id=episode.podcast_id).first()

            # Ensure the podcast exists and associate it with the episode
            if podcast:
                episode._podcast = podcast  # Associate the episode with its podcast
                episode.podcast_id = podcast._id  # Ensure the podcast_id is set correctly

                scm.session.add(episode)  # Add episode to session only if podcast is valid
            else:
                print(f"Podcast with id {episode.podcast_id} not found for episode {episode._title}")
                # Handle the case where the podcast is not found (optional)
        scm.commit()


def populate_database(repo: SqlAlchemyRepository, data_path):
    load_data(data_path, repo)

