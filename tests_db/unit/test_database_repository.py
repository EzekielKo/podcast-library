import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from podcast.adapters.orm import metadata, map_model_to_tables
from podcast.adapters.databaseRepository import SqlAlchemyRepository
from podcast.domainmodel.model import Author, Podcast, Episode, Category, Review, User, Playlist



@pytest.fixture
def database_repo(session_factory):
    return SqlAlchemyRepository(session_factory)


# Helper function to find the next available id
def find_next_id(database_repo, model_class):
    existing_items = database_repo._session_cm.session.query(model_class).all()
    occupied_ids = [item.id for item in existing_items]

    new_id = 1
    while new_id in occupied_ids:
        new_id += 1
    return new_id


def test_add_podcast(database_repo):
    # Find the next available author id
    author_id = find_next_id(database_repo, Author)

    # Find the next available podcast id
    podcast_id = find_next_id(database_repo, Podcast)

    # Create the new author and podcast with the available ids
    author = Author(author_id, "John Doe")
    podcast = Podcast(podcast_id, author, "Test Podcast", None, "Test description")

    # Add the podcast to the repository
    database_repo.add_podcast(podcast)

    # Retrieve and assert that the podcast was added correctly
    retrieved = database_repo.get_podcast(podcast_id)
    assert retrieved == podcast


def test_add_episode(database_repo):
    # Find the next available ids
    author_id = find_next_id(database_repo, Author)
    podcast_id = find_next_id(database_repo, Podcast)
    episode_id = find_next_id(database_repo, Episode)

    # Create the author, podcast, and episode
    author = Author(author_id, "John Doe")
    podcast = Podcast(podcast_id, author, "Test Podcast", None, "Test description")
    episode = Episode(episode_id, podcast.id, 300, "Episode 1", "http://audio_link.com", "Episode description")

    # Add podcast and episode to the repository
    database_repo.add_podcast(podcast)
    database_repo.add_episode(episode)

    # Retrieve and check the episode
    retrieved = database_repo.get_episode(episode_id)
    assert retrieved == episode


def test_add_author(database_repo):
    # Find the next available author id
    author_id = find_next_id(database_repo, Author)

    # Create and add the author
    author = Author(author_id, "Jane Doe")
    database_repo.add_author(author)

    # Retrieve and check the author
    retrieved = database_repo.get_author(author_id)
    assert retrieved == author


def test_add_category(database_repo):
    # Find the next available category id
    category_id = find_next_id(database_repo, Category)

    # Create and add the category
    category = Category(category_id, "Technology")
    database_repo.add_category(category)

    # Retrieve and check the category
    retrieved = database_repo.get_category(category_id)
    assert retrieved == category


def test_add_review(database_repo):
    # Find the next available ids
    author_id = find_next_id(database_repo, Author)
    podcast_id = find_next_id(database_repo, Podcast)
    user_id = find_next_id(database_repo, User)
    review_id = find_next_id(database_repo, Review)

    # Create and add the entities
    author = Author(author_id, "John Doe")
    podcast = Podcast(podcast_id, author, "Test Podcast", None, "Test description")
    user = User(user_id, "user1", "password")
    review = Review(review_id, podcast, user, 5, "Excellent podcast!")

    database_repo.add_podcast(podcast)
    database_repo.add_user(user)
    database_repo.add_review(review)

    # Retrieve and check the review
    retrieved = database_repo.get_review(review_id)
    assert retrieved == review


def test_add_playlist(database_repo):
    # Find the next available ids
    user_id = find_next_id(database_repo, User)
    playlist_id = find_next_id(database_repo, Playlist)

    # Create and add the user and playlist
    user = User(user_id, "user1", "password")
    playlist = Playlist(playlist_id, user, "My Playlist")

    database_repo.add_user(user)
    database_repo.add_playlist(playlist)

    # Retrieve and check the playlist
    retrieved = database_repo.get_playlist(playlist_id)
    assert retrieved == playlist


def test_add_user(database_repo):
    # Find the next available user id
    user_id = find_next_id(database_repo, User)

    # Create and add the user
    user = User(user_id, "user1", "password")
    database_repo.add_user(user)

    # Retrieve and check the user
    retrieved = database_repo.get_user(user_id)
    assert retrieved == user


def test_get_user_by_username(database_repo):
    # Find the next available user id
    user_id = find_next_id(database_repo, User)

    # Create and add the user
    user = User(user_id, "user1", "password")
    database_repo.add_user(user)

    # Retrieve and check the user by username
    retrieved = database_repo.get_user_by_username("user1")
    assert retrieved == user


def test_add_episode_to_playlist(database_repo):
    # Find the next available ids
    author_id = find_next_id(database_repo, Author)
    podcast_id = find_next_id(database_repo, Podcast)
    episode_id = find_next_id(database_repo, Episode)
    user_id = find_next_id(database_repo, User)
    playlist_id = find_next_id(database_repo, Playlist)

    # Create and add the entities
    author = Author(author_id, "Author 1")
    podcast = Podcast(podcast_id, author, "Podcast 1")
    episode = Episode(episode_id, podcast.id, 120, "Episode 1")
    user = User(user_id, "user1", "password")
    playlist = Playlist(playlist_id, user, "My Playlist")

    database_repo.add_podcast(podcast)
    database_repo.add_user(user)
    database_repo.add_playlist(playlist)
    database_repo.add_episode(episode)

    # Add episode to playlist
    database_repo.add_episode_to_playlist(episode, playlist)

    # Assert the episode is in the playlist
    assert episode in playlist.episodes
