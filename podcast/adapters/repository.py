import abc
from typing import List

from podcast.domainmodel.model import Podcast, Episode, Author, Category, Review, Playlist, User

class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    
    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        """ Adds a Podcast to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast(self, podcast_id: int) -> Podcast:
        """ Returns the Podcast with the given id from the repository.

        If no Podcast with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_podcasts(self) -> List[Podcast]:
        """ Returns a list of all Podcasts in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """ Adds an Episode to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode(self, episode_id: int) -> Episode:
        """ Returns the Episode with the given id from the repository.

        If no Episode with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """ Adds an Author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_id: int) -> Author:
        """ Returns the Author with the given id from the repository.

        If no Author with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        """ Adds a Category to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_category(self, category_id: int) -> Category:
        """ Returns the Category with the given id from the repository.

        If no Category with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_categories(self) -> List[Category]:
        """ Returns a list of all Categories in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self, review_id: int) -> Review:
        """ Returns the Review with the given id from the repository.

        If no Review with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_review_id(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, playlist: Playlist):
        """ Adds a Playlist to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist(self, playlist_id: int) -> Playlist:
        """ Returns the Playlist with the given id from the repository.

        If no Playlist with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_id: int) -> User:
        """ Returns the User with the given id from the repository.

        If no User with the given id exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> User:
        """ Returns the User with the given username from the repository.

        If no User with the given username exists, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode_to_playlist(self, episode: Episode, playlist: Playlist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_playlist_id(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_by_user(self, user: User) -> Playlist:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_episode_from_playlist(self, episode: Episode, playlist: Playlist):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review_to_podcast(self, review: Review, podcast: Podcast):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_user_id(self) -> int:
        raise NotImplementedError