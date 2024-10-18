gitfrom datetime import datetime
from unittest.mock import patch, mock_open
import os
import pytest
from podcast.domainmodel.model import Podcast, Episode, Author, Category
from podcast.adapters.datareader.csvdatareader import CSVDataReader

@pytest.fixture
def csv_data_reader():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    return CSVDataReader(data_folder)

def test_set_podcasts(csv_data_reader):
    csv_data_reader.dir_name = os.path.dirname(os.path.abspath(__file__))
    csv_data_reader.parent_dir = os.path.dirname(csv_data_reader.dir_name)
    csv_data_reader.data_folder = os.path.join(csv_data_reader.parent_dir, "unit")
    csv_data_reader.podcasts_filepath = os.path.join(csv_data_reader.data_folder, "podcasts.csv")
    assert csv_data_reader.podcasts_filepath.endswith("podcasts.csv")

def test_set_episodes(csv_data_reader):
    csv_data_reader.dir_name = os.path.dirname(os.path.abspath(__file__))
    csv_data_reader.parent_dir = os.path.dirname(csv_data_reader.dir_name)
    csv_data_reader.data_folder = os.path.join(csv_data_reader.parent_dir, "unit")
    csv_data_reader.episodes_filepath = os.path.join(csv_data_reader.data_folder, "episodes.csv")
    assert csv_data_reader.episodes_filepath.endswith("episodes.csv")

# Tests for reading podcasts
def test_read_podcasts(csv_data_reader):
    mock_csv_data = (
        "id,name,image,description,language,categories,website,author,itunes_id\n"
        "1,Test Podcast,image1.jpg,Description 1,English,Technology|Education,http://testpodcast.com,Author 1,12345\n"
        "2,Another Podcast,image2.jpg,Description 2,Spanish,Science,http://anotherpodcast.com,Author 2,67890"
    )
    
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        csv_data_reader.podcasts_filepath = "fake_path.csv"
        csv_data_reader.read_podcasts()

    assert len(csv_data_reader.podcasts) == 2

    podcast1 = csv_data_reader.podcasts[0]
    assert podcast1.id == 1
    assert podcast1.title == "Test Podcast"
    assert podcast1.image == "image1.jpg"
    assert podcast1.description == "Description 1"
    assert podcast1.language == "English"
    assert podcast1.website == "http://testpodcast.com"
    assert podcast1.itunes_id == 12345
    assert len(podcast1.categories) == 2
    assert podcast1.categories[0].name == "Technology"
    assert podcast1.categories[1].name == "Education"
    assert podcast1.author.name == "Author 1"

    podcast2 = csv_data_reader.podcasts[1]
    assert podcast2.id == 2
    assert podcast2.title == "Another Podcast"
    assert podcast2.image == "image2.jpg"
    assert podcast2.description == "Description 2"
    assert podcast2.language == "Spanish"
    assert podcast2.website == "http://anotherpodcast.com"
    assert podcast2.itunes_id == 67890
    assert len(podcast2.categories) == 1
    assert podcast2.categories[0].name == "Science"
    assert podcast2.author.name == "Author 2"

    assert len(csv_data_reader.authors) == 2
    author_names = {author.name for author in csv_data_reader.authors}
    assert "Author 1" in author_names
    assert "Author 2" in author_names

    assert len(csv_data_reader.categories) == 3
    category_names = {category.name for category in csv_data_reader.categories}
    assert "Technology" in category_names
    assert "Education" in category_names
    assert "Science" in category_names

# Tests for reading episodes
def test_read_episodes(csv_data_reader):
    mock_csv_data = (
        "id,podcast_id,title,audio,audio_length,description,pub_date\n"
        "1,1,Episode 1,audio1.mp3,3600,Description of episode 1,2024-01-01\n"
        "2,1,Episode 2,audio2.mp3,3000,Description of episode 2,2024-01-02"
    )
    
    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        csv_data_reader.episodes_filepath = "fake_path.csv"
        csv_data_reader.read_episodes()

    assert len(csv_data_reader.episodes) == 2

    episode1 = csv_data_reader.episodes[0]
    assert episode1.id == 1
    assert episode1.podcast_id == 1
    assert episode1.title == "Episode 1"
    assert episode1.audio == "audio1.mp3"
    assert episode1.audio_length == 3600
    assert episode1.description == "Description of episode 1"
    assert episode1.pub_date == datetime(2024, 1, 1)

    episode2 = csv_data_reader.episodes[1]
    assert episode2.id == 2
    assert episode2.podcast_id == 1
    assert episode2.title == "Episode 2"
    assert episode2.audio == "audio2.mp3"
    assert episode2.audio_length == 3000
    assert episode2.description == "Description of episode 2"
    assert episode2.pub_date == datetime(2024, 1, 2)


# Tests to check initial state of CSVDataReader
def test_podcasts(csv_data_reader):
    assert csv_data_reader.podcasts == [] 

def test_episodes(csv_data_reader):
    assert csv_data_reader.episodes == []  

def test_authors(csv_data_reader):
    assert csv_data_reader.authors == set()  

def test_categories(csv_data_reader):
    assert csv_data_reader.categories == set() 
