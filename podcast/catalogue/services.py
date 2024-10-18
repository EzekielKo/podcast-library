from typing import List, Dict
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Episode, Author, Category, Review, Playlist, User
from podcast.exceptions import NonExistentEpisodeException, NonExistentPodcastException, UnknownUserException

def get_podcasts_by_letter(letter: str, repo: AbstractRepository) -> Dict:
    letter = letter.upper()

    podcasts = repo.get_all_podcasts()

    if letter == '#':
        filtered_podcasts = [podcast for podcast in podcasts if not podcast.title[0].upper().isalpha()]
    else:
        filtered_podcasts = [podcast for podcast in podcasts if podcast.title.upper().startswith(letter)]

    sorted_podcasts = sorted(filtered_podcasts, key=lambda podcast: podcast.title.upper())

    return {
        'podcasts': [podcast_to_dict(podcast) for podcast in sorted_podcasts],
    }

# Convert model entities to dictionaries
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