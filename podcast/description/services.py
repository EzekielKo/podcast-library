from typing import Dict
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Review, User, Episode, Playlist
from podcast.exceptions import NonExistentEpisodeException, NonExistentPodcastException, UnknownUserException


def get_podcast_data(podcast_id: int, repo: AbstractRepository) -> Dict:
    podcast = repo.get_podcast(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException(f"Podcast with id {podcast_id} does not exist.")
    return podcast_to_dict(podcast)


def get_previous_and_next_podcast_ids(podcast_id: int, repo: AbstractRepository) -> Dict[str, int]:
    podcasts = repo.get_all_podcasts()
    sorted_podcasts = sorted(podcasts, key=lambda podcast: podcast.title.lower())

    previous_id = None
    next_id = None
    for index, podcast in enumerate(sorted_podcasts):
        if podcast.id == podcast_id:
            if index > 0:
                previous_id = sorted_podcasts[index - 1].id
            if index < len(sorted_podcasts) - 1:
                next_id = sorted_podcasts[index + 1].id
            break

    return {
        'previous_id': previous_id,
        'next_id': next_id
    }


def add_review_to_podcast(user: User, rating: int, content: str, podcast: Podcast, repo: AbstractRepository):
    review_id = repo.get_next_review_id()
    review = Review(review_id, podcast, user, rating, content)
    repo.add_review_to_podcast(review, podcast)


def add_episode_to_playlist(playlist: Playlist, episode: Episode, repo: AbstractRepository) -> Playlist:
    repo.add_episode_to_playlist(episode, playlist)

    return playlist

def get_podcast(id: int, repo: AbstractRepository):
    return repo.get_podcast(id)


def get_user_by_username(username: str, repo: AbstractRepository):
    return repo.get_user_by_username(username)


def get_episode(episode_id: int, repo: AbstractRepository):
    return repo.get_episode(episode_id)


def get_user_playlist(user: User, repo: AbstractRepository):
    return repo.get_playlist_by_user(user)


def create_playlist(owner: User, name: str, repo: AbstractRepository):
    playlist_id = repo.get_next_playlist_id()
    playlist = Playlist(playlist_id, owner, name)
    repo.add_playlist(playlist)
    return playlist


def calculate_average_rating(podcast: Podcast) -> float:
    if not podcast.reviews:
        return 0.0
    total_rating = sum([review.rating for review in podcast.reviews])
    average_rating = total_rating / len(podcast.reviews)
    return round(average_rating, 1)  # Round to one decimal place


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
        'categories': [category.name for category in podcast.categories],
        'episodes': sorted(podcast.episodes, key=lambda episode: episode.title),
        'reviews': sorted(podcast.reviews, key=lambda review: review.rating),
        'average_rating': calculate_average_rating(podcast)  # Add average rating here
    }

