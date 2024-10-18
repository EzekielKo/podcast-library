from typing import List, Dict
from podcast.domainmodel.model import Podcast, Episode, Author, Category, Review, Playlist, User
from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._podcasts: Dict[int, Podcast] = {}
        self._episodes: Dict[int, Episode] = {}
        self._authors: Dict[int, Author] = {}
        self._categories: Dict[int, Category] = {}
        self._reviews: Dict[int, Review] = {}
        self._playlists: Dict[int, Playlist] = {}
        self._users: Dict[int, User] = {}
        self._next_user_id = 1
        self._next_playlist_id = 1
        self._next_review_id = 1


    # Podcast methods
    def add_podcast(self, podcast: Podcast):
        self._podcasts[podcast.id] = podcast

    def get_podcast(self, podcast_id: int) -> Podcast:
        return self._podcasts.get(podcast_id)

    def get_all_podcasts(self) -> List[Podcast]:
        return list(self._podcasts.values())

    # Episode methods
    def add_episode(self, episode: Episode):
        self._episodes[episode.id] = episode

    def get_episode(self, episode_id: int) -> Episode:
        return self._episodes.get(episode_id)

    def add_episode_to_playlist(self, episode: Episode, playlist: Playlist):
        playlist.add_episode(episode)

    def remove_episode_from_playlist(self, episode: Episode, playlist: Playlist):
        playlist.remove_episode(episode)

    # Author methods
    def add_author(self, author: Author):
        self._authors[author.id] = author

    def get_author(self, author_id: int) -> Author:
        return self._authors.get(author_id)

    # Category methods
    def add_category(self, category: Category):
        self._categories[category.id] = category

    def get_category(self, category_id: int) -> Category:
        return self._categories.get(category_id)

    def get_all_categories(self) -> List[Category]:
        return list(self._categories.values())

    # Review methods
    def add_review(self, review: Review):
        self._reviews[review.id] = review
        reviewed_item = review.podcast

        if isinstance(reviewed_item, Podcast):
            podcast = self.get_podcast(reviewed_item.id)
            if podcast:
                podcast.add_review(review)

    def add_review_to_podcast(self, review: Review, podcast: Podcast):
        podcast.add_review(review)
        self._reviews[review.id] = review


    def get_next_review_id(self) -> int:
        review_id = self._next_review_id
        self._next_review_id += 1
        return review_id

    def get_review(self, review_id: int) -> Review:
        return self._reviews.get(review_id)

    def get_reviews_for_podcast(self, podcast_id: int) -> List[Review]:
        podcast = self.get_podcast(podcast_id)
        return podcast.reviews if podcast else []

    # Playlist methods
    def add_playlist(self, playlist: Playlist):
        self._playlists[playlist.id] = playlist

    def get_playlist(self, playlist_id: int) -> Playlist:
        return self._playlists.get(playlist_id)

    def get_next_playlist_id(self) -> int:
        playlist_id = self._next_playlist_id
        self._next_playlist_id += 1
        return playlist_id

    def get_playlist_by_user(self, user: User) -> Playlist:
        return next((playlist for playlist in self._playlists.values() if playlist.owner == user), None)

    # User methods
    def add_user(self, user: User):
        self._users[user.id] = user

    def get_user(self, user_id: int) -> User:
        return self._users.get(user_id)

    def get_next_user_id(self) -> int:
        user_id = self._next_review_id
        self._next_review_id += 1
        return user_id

    def get_user_by_username(self, username: str) -> User:
        return next((user for user in self._users.values() if user.username == username), None)

def load_data(self, data_path):
# Initialize the CSVDataReader
    csv_reader = CSVDataReader(data_path)
    csv_reader.read_podcasts()
    csv_reader.read_episodes()

    # Add podcasts, authors, and categories to the repository
    for podcast in csv_reader.podcasts:
        self.add_podcast(podcast)

    for author in csv_reader.authors:
        self.add_author(author)

    for category in csv_reader.categories:
        self.add_category(category)
    # Add episodes to the repository
    for episode in csv_reader.episodes:
        self.add_episode(episode)

def populate(self,data_path):
    load_data(self, data_path)
    # Link episodes to their respective podcasts:
    for episode in self._episodes.values():
        podcast = self.get_podcast(episode.podcast_id)
        if podcast:
            podcast.add_episode(episode)