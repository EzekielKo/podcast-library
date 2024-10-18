import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from datetime import date, datetime


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user(in_memory_repo):
    return User(in_memory_repo.get_next_user_id(), "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)

@pytest.fixture
def my_episode():
    return Episode(1, 10, 300, "Episode Title", "http://example.com/audio.mp3", "An episode description", date(2023, 8, 14))
    

def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization(in_memory_repo):
    user1 = User( in_memory_repo.get_next_user_id(), "shyamli", "pw12345")
    user2 = User( in_memory_repo.get_next_user_id(),"asma", "pw67890")
    user3 = User(in_memory_repo.get_next_user_id(), "jenny  ", "pw87465")
    assert repr(user1) == f"<User {user1.id}: shyamli>"
    assert repr(user2) == f"<User {user2.id}: asma>"
    assert repr(user3) == f"<User {user3.id}: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User( in_memory_repo.get_next_user_id(),"xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User( in_memory_repo.get_next_user_id(),"    ", "qwerty12345")


def test_user_hash(in_memory_repo):
    user1 = User( in_memory_repo.get_next_user_id(),"   Shyamli", "pw12345")
    user2 = User( in_memory_repo.get_next_user_id(),"asma", "pw67890")
    user3 = User( in_memory_repo.get_next_user_id(),"JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt(in_memory_repo):
    user1 = User(in_memory_repo.get_next_user_id(), "Shyamli", "pw12345")
    user2 = User( in_memory_repo.get_next_user_id(),"asma", "pw67890")
    user3 = User( in_memory_repo.get_next_user_id(),"JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by Shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    user_id = my_subscription.owner.id
    assert repr(my_subscription.owner) == f"<User {user_id}: Shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by Shyamli>"


def test_podcast_subscription_set_owner(my_subscription, in_memory_repo):
    new_user = User(in_memory_repo.get_next_user_id(), "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes
def test_episode_initialization():
    episode = Episode(1, 10, 300, "Episode Title", "http://example.com/example.mp3", "example description", date(2023, 8, 14))
    assert episode.id == 1
    assert episode.podcast_id == 10
    assert episode.audio_length == 300
    assert episode.title == "Episode Title"
    assert episode.audio == "http://example.com/example.mp3"
    assert episode.description == "example description"
    assert episode.pub_date == date(2023, 8, 14)

    with pytest.raises(ValueError):
        Episode(-1, 10, 300, "Title")

    with pytest.raises(ValueError):
        Episode(1, 10, -300, "Title")

    with pytest.raises(ValueError):
        Episode(1, 10, 300, "")
        
def test_episode_set_title():
    episode = Episode(1, 10, 300, "Episode Title")
    
    # test setting a valid title
    episode.title = "New Title"
    assert episode.title == "New Title"

    # test setting empty string
    with pytest.raises(ValueError):
        episode.title = ""

    # Test setting non-string type
    with pytest.raises(ValueError):
        episode.title = 12345
        
def test_episode_audio_setter():
    episode = Episode(1, 10, 300, "Episode Title")
    
    # test setting a valid audio link
    episode.audio = "http://example.com/new_audio.mp3"
    assert episode.audio == "http://example.com/new_audio.mp3"

    # test setting non-string type
    with pytest.raises(ValueError):
        episode.audio = 12345

    # test setting a None value
    episode.audio = None
    assert episode.audio is None
    
def test_episode_audio_length_setter():
    episode = Episode(1, 10, 300, "Episode Title")
    
    # test setting a valid audio length
    episode.audio_length = 400
    assert episode.audio_length == 400

    # test setting negative value
    with pytest.raises(ValueError):
        episode.audio_length = -10

    # test setting non-integer type
    with pytest.raises(ValueError):
        episode.audio_length = "300 seconds"
        
def test_episode_description_setter():
    episode = Episode(1, 10, 300, "Episode Title")
    
    # test setting a valid description
    episode.description = "This is a new description."
    assert episode.description == "This is a new description."

    # test setting an empty description
    episode.description = ""
    assert episode.description == ""

    # test setting non-string type
    with pytest.raises(TypeError):
        episode.description = 12345
        
def test_episode_pub_date_setter():
    episode = Episode(1, 10, 300, "Episode Title")
    
    # test setting a valid publication date
    episode.pub_date = date(2023, 8, 14)
    assert episode.pub_date == date(2023, 8, 14)

    # test setting (non-date type)
    with pytest.raises(TypeError):
        episode.pub_date = "2023-08-14"
        
def test_episode_eq():
    episode1 = Episode(1, 10, 300, "Episode A")
    episode2 = Episode(1, 10, 300, "Episode A")
    episode3 = Episode(2, 10, 300, "Episode B")
    assert episode1 == episode2
    assert episode1 != episode3

def test_episode_lt():
    episode1 = Episode(1, 10, 300, "Episode A", pub_date=date(2023, 8, 14))
    episode2 = Episode(2, 10, 300, "Episode B", pub_date=date(2023, 8, 15))
    assert episode1 < episode2
    assert episode2 > episode1
    
def test_episode_hash():
    episode1 = Episode(1, 10, 300, "Episode A")
    episode2 = Episode(1, 10, 300, "Episode A")
    episode3 = Episode(2, 10, 300, "Episode B")

    # test that two equal episodes have  same hash
    assert hash(episode1) == hash(episode2)

    # Test that different episodes have different hashes
    assert hash(episode1) != hash(episode3)

    # Test that the hash remains consistent 
    original_hash = hash(episode1)
    episode1.title = "New Title"
    assert hash(episode1) == original_hash

    # Test that the hash changes if the ID 
    episode1._id = 3  # Directly changing the ID to simulate a different episode
    assert hash(episode1) != original_hash

def test_review_initialization(my_user, my_podcast):
    review = Review(1, my_podcast, my_user, 5, "example podcast")
    assert review.id == 1
    assert review.podcast == my_podcast
    assert review.user == my_user
    assert review.rating == 5
    assert review.content == "example podcast"

    with pytest.raises(ValueError):
        Review(1, my_podcast, my_user, 6, "content")

    with pytest.raises(ValueError):
        Review(1, my_podcast, my_user, 0, "content")

    with pytest.raises(TypeError):
        Review(1, "podcast", my_user, 5, "content")

    with pytest.raises(ValueError):
        Review(1, my_podcast, my_user, 5, "")
        
def test_review_rating_setter(my_user,my_podcast):
    review = Review(1, my_podcast, my_user, 5, "example podcast")    
    # test setting a valid rating
    review.rating = 4
    assert review.rating != 5
    assert review.rating == 4
    # test setting an invalid rating
    with pytest.raises(ValueError):
        review.rating = 0

    with pytest.raises(ValueError):
        review.rating = 6
        
def test_review_content_setter(my_podcast, my_user):
    review = Review(1, my_podcast, my_user, 5, "example podcast")   
    # test setting a valid content
    review.content = "example content"
    assert review.content == "example content"

    # est setting an invalid content 
    with pytest.raises(ValueError):
        review.content = ""

def test_review_eq(my_user, my_podcast):
    review1 = Review(1, my_podcast, my_user, 5, "Excellent podcast!")
    review2 = Review(1, my_podcast, my_user, 5, "Excellent podcast!")
    review3 = Review(2, my_podcast, my_user, 4, "Great episode!")
    
    # test same id are equal
    assert review1 == review2
    
    # test different ids are not considered equal
    assert review1 != review3

def test_review_lt(my_user, my_podcast):
    review1 = Review(1, my_podcast, my_user, 5, "review A")
    review2 = Review(2, my_podcast, my_user, 4, "review B")

    # test the less than operator
    assert review1 < review2

    # test the greater than operator
    assert review2 > review1

def test_review_hash(my_user, my_podcast, my_episode, in_memory_repo):
    review1 = Review(1, my_podcast, my_user, 5, "review A")
    review2 = Review(1, my_podcast, my_user, 5, "review B")

    user2 = User(in_memory_repo.get_next_user_id(),"user1", "password")
    review3 = Review(2, my_podcast, user2, 5, "review B")

    # Test  equal reviews have same hash
    assert hash(review1) == hash(review2)

    # Test different reviews have different hashes
    assert hash(review1) != hash(review3)

    # Test that hash remains consistent 
    original_hash = hash(review1)
    review1.rating = 4  
    assert hash(review1) == original_hash

    # test that hash changes if ID changes
    review1._id = 3 
    assert hash(review1) != original_hash


 #fixtures for easier implementation of tests for playlist class   
@pytest.fixture
def my_episode1():
    return Episode(1, 10, 300, "sample episode 1")

@pytest.fixture
def my_episode2():
    return Episode(2, 10, 350, "sample episode 2")

@pytest.fixture
def my_playlist(my_user, my_episode1):
    return Playlist(1, my_user, "My Playlist", [my_episode1])

def test_playlist_initialization(my_user, my_episode1):
    playlist = Playlist(1, my_user, "sample playlist", [my_episode1])
    assert playlist.id == 1
    assert playlist.owner == my_user
    assert playlist.name == "sample playlist"
    assert len(playlist.episodes) == 1
    assert playlist.episodes[0] == my_episode1

    # test initializing with no episodes
    empty_playlist = Playlist(2, my_user, "empty playlist")
    assert empty_playlist.id == 2
    assert len(empty_playlist.episodes) == 0

def test_playlist_name_setter(my_playlist):
    # test setting a valid name
    my_playlist.name = "new playlist name"
    assert my_playlist.name == "new playlist name"

    # test setting empty string
    with pytest.raises(ValueError):
        my_playlist.name = ""

    # test setting non-string type
    with pytest.raises(ValueError):
        my_playlist.name = 12345

def test_playlist_add_episode(my_playlist, my_episode2):
    # add a new episode
    my_playlist.add_episode(my_episode2)
    assert my_episode2 in my_playlist.episodes
    assert len(my_playlist.episodes) == 2

    # try adding the same episode again
    my_playlist.add_episode(my_episode2)
    assert len(my_playlist.episodes) == 2  

def test_playlist_remove_episode(my_playlist, my_episode1, my_episode2):
    # remove an episode
    my_playlist.remove_episode(my_episode1)
    assert my_episode1 not in my_playlist.episodes
    assert len(my_playlist.episodes) == 0

    # try removing an episode that doesn't exist
    my_playlist.remove_episode(my_episode2)
    assert len(my_playlist.episodes) == 0  

def test_playlist_eq(my_playlist, my_user):
    playlist2 = my_playlist
    playlist3 = Playlist(2, my_user, "playlist 2")

    # Test equality based on id
    assert my_playlist == playlist2
    assert my_playlist != playlist3

def test_playlist_lt(my_user, my_episode1, my_episode2):
    playlist1 = Playlist(1, my_user, "Playlist 1", [my_episode1])
    playlist2 = Playlist(2, my_user, "Playlist 2", [my_episode1, my_episode2])

    assert playlist1 < playlist2
    assert playlist2 > playlist1

def test_playlist_hash(my_playlist):
    # test that the hash is based on the playlist id
    playlist1 = Playlist(my_playlist.id, my_playlist.owner, my_playlist.name)
    assert hash(my_playlist) == hash(playlist1)

    # Change playlist id and check that the hash is different
    my_playlist._id = 2
    assert hash(my_playlist) != hash(playlist1)