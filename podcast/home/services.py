from typing import List, Dict
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_homepage_podcasts(repo: AbstractRepository) -> Dict:
   podcasts = repo.get_all_podcasts()
   return {
       'podcasts': [podcast_to_dict(podcast) for podcast in podcasts if podcast.id <= 10]
   }

def podcast_to_dict(podcast: Podcast) -> Dict:
   return {
       'id': podcast.id,
       'title': podcast.title,
       'author': podcast.author.name,
       'image': podcast.image,
       'description': podcast.description,
       'website': podcast.website,
       'itunes_id': podcast.itunes_id,
       'language': podcast.language,
   }

def podcasts_to_dict(podcasts: List[Podcast]) -> List[Dict]:
   return [podcast_to_dict(podcast) for podcast in podcasts]