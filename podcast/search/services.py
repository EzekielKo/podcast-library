from typing import List, Dict
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

def get_podcasts_from_title(title: str, repo: AbstractRepository) -> List[Podcast]:
   podcasts = repo.get_all_podcasts()
   return sorted([podcast for podcast in podcasts if title.lower() in podcast.title.lower()])

def get_podcasts_from_author(author: str, repo: AbstractRepository) -> List[Podcast]:
   podcasts = repo.get_all_podcasts()
   return sorted([podcast for podcast in podcasts if author.lower() in podcast.author.name.lower()])

def get_podcasts_from_category(category: str, repo: AbstractRepository) -> List[Podcast]:
   podcasts = repo.get_all_podcasts()
   return sorted([podcast for podcast in podcasts if any(category.lower() in cat.name.lower() for cat in podcast.categories)])

def get_podcasts_from_language(language: str, repo: AbstractRepository) -> List[Podcast]:
   podcasts = repo.get_all_podcasts()
   return sorted([podcast for podcast in podcasts if language.lower() in podcast.language.lower()])


def get_page(page: int, podcasts: List[Podcast]):
    items_per_page = 10
    page = int(page)

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    return podcasts[start_index:end_index]

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
