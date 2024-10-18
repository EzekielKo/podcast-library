import pytest
from sqlalchemy.exc import IntegrityError
from podcast.domainmodel.model import Author, Podcast, Category, User, Playlist, Episode, Review


def insert_user(empty_session, values=None):
    new_name = "test_user"
    new_password = "password"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username', {'username': new_name}).fetchone()
    return row[0]


def insert_podcast(empty_session, author_id, title="Sample Podcast"):
    empty_session.execute(
        'INSERT INTO podcasts (author_id, title, description) VALUES (:author_id, :title, "Description of the podcast.")',
        {'author_id': author_id, 'title': title}
    )
    row = empty_session.execute('SELECT id from podcasts where title = :title', {'title': title}).fetchone()
    return row[0]


def insert_author(empty_session, name="Test Author"):
    empty_session.execute('INSERT INTO authors (name) VALUES (:name)', {'name': name})
    row = empty_session.execute('SELECT id from authors where name = :name', {'name': name}).fetchone()
    return row[0]


def insert_category(empty_session, name="Category"):
    empty_session.execute('INSERT INTO categories (name) VALUES (:name)', {'name': name})
    row = empty_session.execute('SELECT id from categories where name = :name', {'name': name}).fetchone()
    return row[0]


def test_saving_of_user(empty_session):
    user = User(1,"test_user", "password")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("test_user", "password")]


def test_saving_of_user_with_duplicate_username(empty_session):
    insert_user(empty_session, ("duplicate_user", "password"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(2,"duplicate_user", "new_password")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_user(empty_session):
    user_key = insert_user(empty_session, ("test_user", "password"))
    user = empty_session.query(User).filter(User._id == user_key).one()
    assert user._username == "test_user"
    assert user._password == "password"


def test_saving_of_author(empty_session):
    author = Author(1, "Sample Author")
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT name FROM authors'))
    assert rows == [("Sample Author",)]


def test_loading_of_author(empty_session):
    author_key = insert_author(empty_session, "Author Test")
    author = empty_session.query(Author).filter(Author._id == author_key).one()

    assert author._name == "Author Test"


def test_saving_of_podcast(empty_session):
    author_key = insert_author(empty_session, "Author Test")
    podcast = Podcast(1, empty_session.query(Author).get(author_key), "Test Podcast", None, "Podcast description")
    empty_session.add(podcast)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, description FROM podcasts'))
    assert rows == [("Test Podcast", "Podcast description")]


def test_loading_of_podcast(empty_session):
    author_key = insert_author(empty_session, "Author Test")
    podcast_key = insert_podcast(empty_session, author_key)

    podcast = empty_session.query(Podcast).get(podcast_key)
    assert podcast._title == "Sample Podcast"
    assert podcast._author._name == "Author Test"


def test_saving_and_loading_playlist(empty_session):
    user_key = insert_user(empty_session, ("playlist_user", "password"))
    user = empty_session.query(User).get(user_key)

    playlist = Playlist(1, user, "My Playlist")
    empty_session.add(playlist)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT name FROM playlists'))
    assert rows == [("My Playlist",)]

    playlist_from_db = empty_session.query(Playlist).get(1)
    assert playlist_from_db._name == "My Playlist"
    assert playlist_from_db._owner._username == "playlist_user"


def test_saving_and_loading_review(empty_session):
    author_key = insert_author(empty_session, "Author Review Test")
    podcast_key = insert_podcast(empty_session, author_key)
    user_key = insert_user(empty_session, ("review_user", "password"))

    podcast = empty_session.query(Podcast).get(podcast_key)
    user = empty_session.query(User).get(user_key)
    review = Review(1, podcast, user, 5, "Great Podcast!")

    empty_session.add(review)
    empty_session.commit()

    review_from_db = empty_session.query(Review).get(1)
    assert review_from_db._rating == 5
    assert review_from_db._content == "Great Podcast!"
    assert review_from_db._podcast._title == "Sample Podcast"
    assert review_from_db._user._username == "review_user"


def test_adding_episode_to_playlist(empty_session):
    author_key = insert_author(empty_session, "Author Playlist Test")
    podcast_key = insert_podcast(empty_session, author_key)
    episode = Episode(1, podcast_key, 180, "Test Episode", "http://audio_link")

    user_key = insert_user(empty_session, ("playlist_user", "password"))
    user = empty_session.query(User).get(user_key)

    playlist = Playlist(1, user, "Test Playlist")
    playlist._episodes.append(episode)

    empty_session.add(playlist)
    empty_session.commit()

    playlist_from_db = empty_session.query(Playlist).get(1)
    assert len(playlist_from_db._episodes) == 1
    assert playlist_from_db._episodes[0]._title == "Test Episode"


def test_saving_tagged_podcast(empty_session):
    author_key = insert_author(empty_session)
    podcast_key = insert_podcast(empty_session, author_key)
    category_key = insert_category(empty_session)

    podcast = empty_session.query(Podcast).get(podcast_key)
    category = empty_session.query(Category).get(category_key)

    podcast.categories.append(category)

    empty_session.add(podcast)
    empty_session.commit()

    podcast_from_db = empty_session.query(Podcast).get(podcast_key)
    assert len(podcast_from_db.categories) == 1
    assert podcast_from_db.categories[0]._name == "Category"
