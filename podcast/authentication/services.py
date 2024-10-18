from werkzeug.security import generate_password_hash, check_password_hash

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):

    user = repo.get_user_by_username(username)
    if user is not None:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)

    user = User(repo.get_next_user_id(), username, password_hash)
    repo.add_user(user)

def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user_by_username(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    user = repo.get_user_by_username(user_name)
    if user is None:
        raise UnknownUserException()

    if not check_password_hash(user.password, password):
        raise AuthenticationException()


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.username,
        'password': user.password
    }
    return user_dict
