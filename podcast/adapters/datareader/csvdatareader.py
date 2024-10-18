import os
import csv
from datetime import datetime

from podcast.domainmodel.model import Podcast, Episode, Author, Category

class CSVDataReader:
    def __init__(self, data_folder: str):
        # Define file paths
        dir_name = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(dir_name)
        self.podcasts_filepath = os.path.join(data_folder, "podcasts.csv")
        self.episodes_filepath = os.path.join(data_folder, "episodes.csv")
        
        # Initialise
        self.podcasts = []
        self.episodes = []
        self.authors = set()
        self.categories = set()

    def read_podcasts(self):
        # Read podcasts from CSV and create Podcast objects
        with open(self.podcasts_filepath, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                podcast_id, podcast_title, podcast_image, podcast_description, podcast_language, podcast_categories, \
                    podcast_website, podcast_author, podcast_itunes_id = row

                # convert to integer
                podcast_id = int(podcast_id)
                podcast_itunes_id = int(podcast_itunes_id) if podcast_itunes_id else None

                if podcast_author:
                    author = Author(podcast_id, podcast_author)
                    self.authors.add(author)

                # Create Podcast object
                podcast = Podcast(podcast_id, author, podcast_title, podcast_image, podcast_description,
                                  podcast_website, podcast_itunes_id, podcast_language)

                self.podcasts.append(podcast)

                categories_list = podcast_categories.split("|")
                for category_name in categories_list:
                    category_name = category_name.strip()
                    category_id = len(self.categories) + 1  # Unique ID for the category
                    category = Category(category_id, category_name)
                    self.categories.add(category)
                    podcast.add_category(category)


    def read_episodes(self):
        # Read episodes from CSV and create Episode objects
        with open(self.episodes_filepath, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                episode_id, episode_podcast_id, episode_title, episode_audio, \
                    episode_audio_length, episode_description, episode_pub_date = row

                # Convert values to integer
                episode_id = int(episode_id) if episode_id else None
                episode_podcast_id = int(episode_podcast_id) if episode_podcast_id else None
                episode_audio_length = int(episode_audio_length) if episode_audio_length else None

                # Preprocess pub_date to replace '+00' with '+0000'
                if episode_pub_date.endswith('+00'):
                    episode_pub_date = episode_pub_date.replace('+00', '+0000')

                # Convert pub_date from string to datetime using strptime
                try:
                    episode_pub_date = datetime.strptime(episode_pub_date, '%Y-%m-%d %H:%M:%S%z')
                except ValueError:
                    episode_pub_date = datetime.strptime(episode_pub_date, '%Y-%m-%d')

                # Create Episode object
                episode = Episode(episode_id, episode_podcast_id, episode_audio_length, episode_title,
                                  episode_audio, episode_description, episode_pub_date)
                self.episodes.append(episode)

'''
testobject = CSVDataReader()
testobject.read_podcasts()
#testobject.read_episodes()
sorted_podcasts = sorted(testobject.podcasts, key=lambda podcast: podcast.title)
#output = testobject.podcasts[0].categories
print(sorted_podcasts)
'''
