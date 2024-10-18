from podcast.domainmodel.model import Podcast, Author, Category, Episode, User, Review
from podcast.adapters.memoryRepository import MemoryRepository, populate
from podcast.catalogue.services import get_podcasts_by_letter
from podcast.description.services import get_podcast_data, get_previous_and_next_podcast_ids, add_review_to_podcast, create_playlist, calculate_average_rating
from podcast.exceptions import NonExistentEpisodeException, NonExistentPodcastException, UnknownUserException
from podcast.playlist.services import get_user_playlist, get_user_by_username, remove_from_playlist
from podcast.authentication.services import add_user, authenticate_user, AuthenticationException, UnknownUserException
from podcast.search.services import get_podcasts_from_title, get_podcasts_from_language, get_podcasts_from_author, get_podcasts_from_category, get_page

from werkzeug.security import  check_password_hash


import pytest


@pytest.fixture
def user(in_memory_repo):
    user = user = User(in_memory_repo.get_next_user_id(),"Shyamli", "pw12345")
    return user

@pytest.fixture
def playlist(in_memory_repo, user):
    playlist = create_playlist(user, "Shyamli's playlist", in_memory_repo)
    return playlist


@pytest.fixture()
def podcast():
    author = Author(1, 'author1')
    return Podcast(1, author, "Podcast1", "image", "description1", "website1", 1, "language1")

@pytest.fixture
def review(in_memory_repo, user, podcast):
    review = Review(1, podcast, user, 3, "content1")
    return review


def test_can_get_podcast_description(in_memory_repo):
    podcast_id = 1

    podcast_as_dict = get_podcast_data(podcast_id, in_memory_repo)

    assert podcast_as_dict['id'] == podcast_id
    assert podcast_as_dict['title'] == 'D-Hour Radio Network'
    assert podcast_as_dict['author'] == 'D Hour Radio Network'
    assert podcast_as_dict['language'] == 'English'
    assert len(podcast_as_dict['episodes']) > 0
    
    podcast_id = 2
    podcast_as_dict = get_podcast_data(podcast_id, in_memory_repo)
    
    assert podcast_as_dict['id'] == podcast_id
    assert podcast_as_dict['title'] == 'Brian Denny Radio'
    assert podcast_as_dict['author'] == 'Brian Denny'
    assert podcast_as_dict['language'] == 'English'
    assert len(podcast_as_dict['episodes']) > 0

def test_get_previous_and_next_podcast_ids(in_memory_repo):
    podcast_id = 1  

    nav_ids = get_previous_and_next_podcast_ids(podcast_id, in_memory_repo)

    assert nav_ids['previous_id'] == 665  
    assert nav_ids['next_id'] == 526  

    podcast_id = 2  

    nav_ids = get_previous_and_next_podcast_ids(podcast_id, in_memory_repo)

    assert nav_ids['previous_id'] == 898  
    assert nav_ids['next_id'] == 10  

    podcast_id = 3  

    nav_ids = get_previous_and_next_podcast_ids(podcast_id, in_memory_repo)

    assert nav_ids['previous_id'] == 749 
    assert nav_ids['next_id'] == 980  

def test_cannot_get_podcast_description_with_non_existent_id(in_memory_repo):
    podcast_id = -1  # Non-existent ID

    with pytest.raises(NonExistentPodcastException):
        get_podcast_data(podcast_id, in_memory_repo)


def test_get_podcasts_by_letter(in_memory_repo):
    letter = 'S'

    podcasts_as_dict = get_podcasts_by_letter(letter, in_memory_repo)

    assert len(podcasts_as_dict['podcasts']) > 0
    for p in podcasts_as_dict['podcasts']:
        assert p['title'].upper().startswith(letter.upper())


def test_get_podcasts_by_letter_with_no_matches(in_memory_repo):
    letter = '/'  # Assuming no podcast title starts with '/'

    podcasts_as_dict = get_podcasts_by_letter(letter, in_memory_repo)

    assert len(podcasts_as_dict['podcasts']) == 0


def test_get_user_playlist(in_memory_repo, user, playlist):
    playlist1 = get_user_playlist(user, in_memory_repo)

    assert playlist1 is not None
    assert playlist1 == playlist


def test_remove_from_playlist(in_memory_repo, user, playlist):
    episode = Episode(1, 1, 60, "Episode1")
    episode_id = 1  # Assuming this episode exists in the user's playlist

    playlist.add_episode(episode)
    result = remove_from_playlist(user, episode_id, in_memory_repo)

    assert result is True  # Assert that the episode was removed
    assert len(playlist.episodes) == 0

def test_add_review_to_podcast(in_memory_repo, user, podcast):
    rating = 4
    content = "Great podcast!"

    add_review_to_podcast(user, rating, content, podcast, in_memory_repo)
    print(podcast.reviews)

    assert len(podcast.reviews) > 0
    assert podcast.reviews[-1].content == content


def test_create_playlist(in_memory_repo, user):
    playlist_name = 'My Favorite Podcasts'

    playlist1 = create_playlist(user, playlist_name, in_memory_repo)

    assert playlist1 is not None
    assert playlist1.name == playlist_name
    assert playlist1.owner == user


def test_calculate_average_rating(in_memory_repo, podcast, user):
    average_rating = calculate_average_rating(podcast)

    assert isinstance(average_rating, float)
    assert 0.0 == average_rating  # Rating should be 0

    add_review_to_podcast(user, 4, "content1", podcast, in_memory_repo)
    average_rating = calculate_average_rating(podcast)
    assert isinstance(average_rating, float)
    assert 4.0 == average_rating

    add_review_to_podcast(user, 5, "content1", podcast, in_memory_repo)
    average_rating = calculate_average_rating(podcast)
    assert isinstance(average_rating, float)
    assert 4.5 == average_rating

def test_add_user(in_memory_repo):
    username = 'newuser'
    password = 'password123'

    add_user(username, password, in_memory_repo)

    user1 = get_user_by_username(username, in_memory_repo)

    assert user1 is not None
    assert user1.username == username
    assert check_password_hash(user1.password, password)


def test_authenticate_user_success(in_memory_repo):
    # Set up a known user in the repo
    username = 'testuser'
    password = 'password123'
    add_user(username, password, in_memory_repo)

    try:
        authenticate_user(username, password, in_memory_repo)
        assert True  # If no exception is raised, the test passes
    except AuthenticationException:
        assert False  # Fail the test if authentication fails unexpectedly


def test_authenticate_user_failure(in_memory_repo):
    username = 'testuser'
    password = 'password123'
    add_user(username, password, in_memory_repo)

    wrong_password = 'wrongpassword'
    with pytest.raises(AuthenticationException):
        authenticate_user(username, wrong_password, in_memory_repo)

def test_authenticate_nonexistent_user(in_memory_repo):
    # Test failed authentication for a non-existent user
    username = 'nonexistentuser'
    password = 'password123'

    with pytest.raises(UnknownUserException):
        authenticate_user(username, password, in_memory_repo)

def test_get_podcasts_from_title(in_memory_repo):
    title = "Radio"
    podcasts = get_podcasts_from_title(title, in_memory_repo)

    assert len(podcasts) > 0
    for podcast in podcasts:
        assert title.lower() in podcast.title.lower() #tests all podcast titles contain input


def test_get_podcasts_from_author(in_memory_repo):
    author_name = "Denny"
    podcasts = get_podcasts_from_author(author_name, in_memory_repo)

    assert len(podcasts) > 0
    for podcast in podcasts:
        assert author_name.lower() in podcast.author.name.lower()


def test_get_podcasts_from_category(in_memory_repo):
    category_name = "News"  # Assuming there's a category named "News"
    podcasts = get_podcasts_from_category(category_name, in_memory_repo)

    assert len(podcasts) > 0  # Ensure that we get some results
    for podcast in podcasts:
        assert any(category_name.lower() in cat.name.lower() for cat in podcast.categories)


def test_get_podcasts_from_language(in_memory_repo):
    language = "English"
    podcasts = get_podcasts_from_language(language, in_memory_repo)

    assert len(podcasts) > 0  # Ensure that we get some results
    for podcast in podcasts:
        assert language.lower() in podcast.language.lower()

def test_get_page(in_memory_repo):
    podcasts = in_memory_repo.get_all_podcasts()
    page = 1
    items_per_page = 10

    paginated_podcasts = get_page(page, podcasts)

    assert len(paginated_podcasts) <= items_per_page  # Ensure only 10 or fewer items are returned
    assert paginated_podcasts == podcasts[0:items_per_page]
