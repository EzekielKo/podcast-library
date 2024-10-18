from typing import Dict
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Review, User, Episode, Playlist


def get_user_playlist(user, repo: AbstractRepository):
    if user is None:
        return []
    return repo.get_playlist_by_user(user)


def get_user_by_username(username: str, repo: AbstractRepository):
    return repo.get_user_by_username(username)


def remove_from_playlist(user, episode_id, repo: AbstractRepository):
    if user is None:
        return False
    playlist = repo.get_playlist_by_user(user)
    episode_to_remove = next((ep for ep in playlist.episodes if ep.id == episode_id), None)
    if episode_to_remove:
        repo.remove_episode_from_playlist(episode_to_remove, playlist)
        return True
    return False


