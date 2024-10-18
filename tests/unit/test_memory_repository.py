import pytest
from datetime import date

from podcast.domainmodel.model import Podcast, Episode, Author, Category, Review, Playlist, User
from podcast.adapters.memoryRepository import MemoryRepository

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    return repo

# User Tests
def test_repository_can_add_a_user(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(), "Shyamli", "pw12345")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user(user.id) == user

def test_repository_can_retrieve_a_user_by_username(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    in_memory_repo.add_user(user)
    retrieved_user = in_memory_repo.get_user_by_username("Shyamli")
    assert retrieved_user == user

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user_by_username("gdsfgdsfgsdfgsdfgdsf")
    assert user is None

# Podcast Tests
def test_repository_can_add_a_podcast(in_memory_repo):
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    in_memory_repo.add_podcast(podcast)
    assert in_memory_repo.get_podcast(podcast.id) == podcast

def test_repository_can_retrieve_a_podcast(in_memory_repo):
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    in_memory_repo.add_podcast(podcast)
    retrieved_podcast = in_memory_repo.get_podcast(1)
    assert retrieved_podcast == podcast

def test_repository_can_retrieve_all_podcasts(in_memory_repo):
    author = Author(1, "Author1")
    podcast1 = Podcast(1, author, "Podcast1")
    podcast2 = Podcast(2, author, "Podcast2")
    in_memory_repo.add_podcast(podcast1)
    in_memory_repo.add_podcast(podcast2)
    podcasts = in_memory_repo.get_all_podcasts()
    assert len(podcasts) == 2
    assert podcast1 in podcasts
    assert podcast2 in podcasts

# Episode Tests
def test_repository_can_add_an_episode(in_memory_repo):
    episode = Episode(1, 1, 60, "Episode1")
    in_memory_repo.add_episode(episode)
    assert in_memory_repo.get_episode(episode.id) == episode

def test_repository_can_retrieve_an_episode(in_memory_repo):
    episode = Episode(1, 1, 60, "Episode1")
    in_memory_repo.add_episode(episode)
    retrieved_episode = in_memory_repo.get_episode(1)
    assert retrieved_episode == episode

# Author Tests
def test_repository_can_add_an_author(in_memory_repo):
    author = Author(1, "Author1")
    in_memory_repo.add_author(author)
    assert in_memory_repo.get_author(author.id) == author

def test_repository_can_retrieve_an_author(in_memory_repo):
    author = Author(1, "Author1")
    in_memory_repo.add_author(author)
    retrieved_author = in_memory_repo.get_author(1)
    assert retrieved_author == author

# Category Tests
def test_repository_can_add_a_category(in_memory_repo):
    category = Category(1, "Category1")
    in_memory_repo.add_category(category)
    assert in_memory_repo.get_category(category.id) == category

def test_repository_can_retrieve_a_category(in_memory_repo):
    category = Category(1, "Category1")
    in_memory_repo.add_category(category)
    retrieved_category = in_memory_repo.get_category(1)
    assert retrieved_category == category

def test_repository_can_retrieve_all_categories(in_memory_repo):
    category1 = Category(1, "Category1")
    category2 = Category(2, "Category2")
    in_memory_repo.add_category(category1)
    in_memory_repo.add_category(category2)
    categories = in_memory_repo.get_all_categories()
    assert len(categories) == 2
    assert category1 in categories
    assert category2 in categories

# Review Tests
def test_repository_can_add_a_review(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    review = Review(1, podcast, user, 5, "Great Podcast!")
    in_memory_repo.add_review(review)
    assert in_memory_repo.get_review(review.id) == review

def test_repository_can_retrieve_a_review(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    review = Review(1, podcast, user, 5, "Great Podcast!")
    in_memory_repo.add_review(review)
    retrieved_review = in_memory_repo.get_review(1)
    assert retrieved_review == review


def test_repository_can_add_review_to_podcast(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    review = Review(1, podcast, user, 5, "Great Podcast!")

    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_review_to_podcast(review, podcast)

    assert review in podcast.reviews


def test_repository_can_get_reviews_for_podcast(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    author = Author(1, "Author1")
    podcast = Podcast(1, author, "Podcast1")
    review1 = Review(1, podcast, user, 5, "Great Podcast!")
    review2 = Review(2, podcast, user, 4, "Good Podcast")

    in_memory_repo.add_podcast(podcast)
    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)

    reviews = in_memory_repo.get_reviews_for_podcast(podcast.id)

    assert len(reviews) == 2
    assert review1 in reviews
    assert review2 in reviews

# Playlist Tests
def test_repository_can_add_a_playlist(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    playlist = Playlist(1, user, "My Playlist")
    in_memory_repo.add_playlist(playlist)
    assert in_memory_repo.get_playlist(playlist.id) == playlist

def test_repository_can_retrieve_a_playlist(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    playlist = Playlist(1, user, "My Playlist")
    in_memory_repo.add_playlist(playlist)
    retrieved_playlist = in_memory_repo.get_playlist(1)
    assert retrieved_playlist == playlist


def test_repository_can_add_episode_to_playlist(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    playlist = Playlist(1, user, "My Playlist")
    episode = Episode(1, 1, 60, "Episode1")

    in_memory_repo.add_playlist(playlist)
    in_memory_repo.add_episode(episode)

    in_memory_repo.add_episode_to_playlist(episode, playlist)

    assert episode in playlist.episodes


def test_repository_can_remove_episode_from_playlist(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    playlist = Playlist(1, user, "My Playlist")
    episode = Episode(1, 1, 60, "Episode1")

    in_memory_repo.add_playlist(playlist)
    in_memory_repo.add_episode(episode)

    in_memory_repo.add_episode_to_playlist(episode, playlist)
    in_memory_repo.remove_episode_from_playlist(episode, playlist)

    assert episode not in playlist.episodes


def test_repository_can_get_playlist_by_user(in_memory_repo):
    user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    playlist = Playlist(1, user, "My Playlist")

    in_memory_repo.add_playlist(playlist)
    retrieved_playlist = in_memory_repo.get_playlist_by_user(user)

    assert retrieved_playlist == playlist

# ID Generation Tests
def test_repository_can_generate_next_review_id(in_memory_repo):
    next_id = in_memory_repo.get_next_review_id()
    assert next_id == 1
    next_id = in_memory_repo.get_next_review_id()
    assert next_id == 2

def test_repository_can_generate_next_playlist_id(in_memory_repo):
    next_id = in_memory_repo.get_next_playlist_id()
    assert next_id == 1
    next_id = in_memory_repo.get_next_playlist_id()
    assert next_id == 2