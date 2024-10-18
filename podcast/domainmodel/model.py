from __future__ import annotations
from datetime import date, datetime

from sqlalchemy import Date


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self.reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")
        if review not in self.reviews:
            self.reviews.append(review)

    def remove_review(self, review: Review):
        if review in self.reviews:
            self.reviews.remove(review)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:

    def __init__(self, id: int, username: str, password: str):
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = id
        self._username = username.strip()
        self._password = password
        self._subscription_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def playlists(self) -> list[Playlist]:
        return self._playlists

    def add_episode(self, episode: Episode):
        if episode not in self._subscription_list:
            self._subscription_list.append(episode)
        else:
            return False
        return True

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    # TODO: Complete the implementation of the Episode class.
    def __init__(self, episode_id: int, podcast_id: int, audio_length: int, title: str, audio_link: str = "",
                 description: str = "", pub_date: Date = None):
        validate_non_negative_int(episode_id)
        validate_non_negative_int(podcast_id)
        validate_non_negative_int(audio_length)
        validate_non_empty_string(title, "Episode title")
        self._id = episode_id
        self._podcast_id = podcast_id
        self._title = title.strip()
        self._audio = audio_link
        self._audio_length = audio_length
        self._description = description
        self._pub_date = pub_date

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def podcast_id(self) -> int:
        return self._podcast_id

    @podcast_id.setter
    def podcast_id(self, id: int):
        self._podcast_id = id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        validate_non_empty_string(title, "Episode title")
        self._title = title.strip()

    @property
    def audio(self) -> str:
        return self._audio

    @audio.setter
    def audio(self, audio_link: str):
        if audio_link != None:
            validate_non_empty_string(audio_link, "audio link")
        self._audio = audio_link

    @property
    def audio_length(self) -> int:
        return self._audio_length

    @audio_length.setter
    def audio_length(self, audio_length: int):
        validate_non_negative_int(audio_length)
        self._audio_length = audio_length

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str):
            self._description = description
        else:
            raise (TypeError)

    @property
    def pub_date(self):
        return self._pub_date

    @pub_date.setter
    def pub_date(self, pub_date):
        if isinstance(pub_date, (date, datetime)):
            self._pub_date = pub_date
        else:
            raise TypeError("pub_date must be a Date or DateTime object")

    def __repr__(self):
        return (f"Episode(id={self._id}, podcast_id={self._podcast_id}, title='{self._title}', "
                f"audio_length={self._audio_length}, pub_date={self._pub_date})")

    def __eq__(self, other):
        if isinstance(other, Episode):
            return self._id == other._id and self._podcast_id == other._podcast_id
        return False

    def __lt__(self, other):
        if isinstance(other, Episode):
            return self._pub_date < other._pub_date
        return NotImplemented

    def __hash__(self):
        return hash(self._id)


class Review:
    def __init__(self, review_id: int, podcast: Podcast, user: User, rating: int, content: str):
        validate_non_negative_int(review_id)
        validate_non_negative_int(rating)
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        validate_non_empty_string(content, "Review content")
        if not isinstance(podcast, Podcast):
            raise TypeError("Must be podcast type")

        self._id = review_id
        self._podcast = podcast
        self._user = user
        self._rating = rating
        self._content = content.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def user(self) -> User:
        return self._user

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def content(self) -> str:
        return self._content

    @rating.setter
    def rating(self, new_rating):
        if 1 <= new_rating <= 5:
            self._rating = new_rating
        else:
            raise ValueError("Rating must be between 1 and 5.")

    @content.setter
    def content(self, new_content: str):
        validate_non_empty_string(new_content, "Review description")
        self._content = new_content.strip()

    def __repr__(self):
        return (f"Review(id={self._id}, podcast={self._podcast.id}, user={self._user.username}, "
                f"rating={self._rating}, content='{self._content}')")

    def __eq__(self, other):
        if isinstance(other, Review):
            return self._id == other._id
        return False

    def __lt__(self, other):
        if isinstance(other, Review):
            return self._id < other._id
        return NotImplemented

    def __hash__(self):
        return hash(self._id)


class Playlist:
    def __init__(self, playlist_id: int, owner: User, name: str, episodes: list[Episode] = None):
        validate_non_negative_int(playlist_id)
        validate_non_empty_string(name, "name")

        self._id = playlist_id
        self._owner = owner
        self._name = name.strip()
        self._episodes = episodes if episodes else []

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "name")
        self._name = new_name.strip()

    @property
    def episodes(self) -> list[Episode]:
        return self._episodes

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("expected episode instance.")
        if episode not in self._episodes:
            self._episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._episodes:
            self._episodes.remove(episode)

    def __repr__(self):
        return (f"Playlist(id={self._id}, owner={self._owner.username}, name='{self._name}', "
                f"episodes={[e.id for e in self._episodes]})")

    def __eq__(self, other):
        if isinstance(other, Playlist):
            return self._id == other._id
        return False

    def __lt__(self, other):
        if isinstance(other, Playlist):
            return len(self._episodes) < len(other._episodes)
        return NotImplemented

    def __hash__(self):
        return hash(self._id)

