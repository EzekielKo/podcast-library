from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship, registry

from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
# Create MetaData instance
metadata = MetaData()

# Define tables
authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
)

podcasts_table = Table(
    'podcasts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('author_id', ForeignKey('authors.id'), nullable=False),
    Column('title', String(255), nullable=False),
    Column('image', String(255)),
    Column('description', String),
    Column('website', String(255)),
    Column('itunes_id', Integer),
    Column('language', String(64))
)

categories_table = Table(
    'categories', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', metadata,
    Column('podcast_id', ForeignKey('podcasts.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True)
)

episodes_table = Table(
    'episodes', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id'), nullable=False),
    Column('title', String(255), nullable=False),
    Column('audio_link', String(255)),
    Column('audio_length', Integer, nullable=False),
    Column('description', String),
    Column('pub_date', Date)
)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

subscriptions_table = Table(
    'subscriptions', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('podcast_id', ForeignKey('podcasts.id'), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.id'), nullable=False),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('content', String, nullable=False)
)

playlists_table = Table(
    'playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('owner_id', ForeignKey('users.id'), nullable=False),
    Column('name', String(255), nullable=False)
)

playlist_episodes_table = Table(
    'playlist_episodes', metadata,
    Column('playlist_id', ForeignKey('playlists.id'), primary_key=True),
    Column('episode_id', ForeignKey('episodes.id'), primary_key=True)
)


# Create a registry instance
mapper_registry = registry()

def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.id,
        '_name': authors_table.c.name,
        'podcast_list': relationship(Podcast, back_populates='_author')
    })

    mapper_registry.map_imperatively(Podcast, podcasts_table, properties={
        '_id': podcasts_table.c.id,
        '_author': relationship(Author, back_populates='podcast_list'),
        '_title': podcasts_table.c.title,
        '_image': podcasts_table.c.image,
        '_description': podcasts_table.c.description,
        '_website': podcasts_table.c.website,
        '_itunes_id': podcasts_table.c.itunes_id,
        '_language': podcasts_table.c.language,
        'categories': relationship(Category, secondary=podcast_categories_table, back_populates='podcasts'),
        'episodes': relationship(Episode, back_populates='_podcast'),
        'reviews': relationship(Review, back_populates='_podcast')
    })

    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.id,
        '_name': categories_table.c.name,
        'podcasts': relationship(Podcast, secondary=podcast_categories_table, back_populates='categories')
    })

    mapper_registry.map_imperatively(Episode, episodes_table, properties={
        '_id': episodes_table.c.id,
        '_title': episodes_table.c.title,
        '_audio': episodes_table.c.audio_link,
        '_audio_length': episodes_table.c.audio_length,
        '_description': episodes_table.c.description,
        '_pub_date': episodes_table.c.pub_date,
        '_podcast_id': episodes_table.c.podcast_id,
        '_podcast': relationship(Podcast, back_populates='episodes'),
        'playlists': relationship(Playlist, secondary=playlist_episodes_table, back_populates='_episodes')
    })

    mapper_registry.map_imperatively(User, users_table, properties={
        '_id': users_table.c.id,
        '_username': users_table.c.username,
        '_password': users_table.c.password,
        '_subscription_list': relationship(PodcastSubscription, back_populates='_owner'),
        '_playlists': relationship(Playlist, back_populates='_owner')
    })

    mapper_registry.map_imperatively(PodcastSubscription, subscriptions_table, properties={
        '_id': subscriptions_table.c.id,
        '_owner': relationship(User, back_populates='_subscription_list'),
        '_podcast': relationship(Podcast)
    })

    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_id': reviews_table.c.id,
        '_podcast': relationship(Podcast, back_populates='reviews'),
        '_user': relationship(User),
        '_rating': reviews_table.c.rating,
        '_content': reviews_table.c.content
    })

    mapper_registry.map_imperatively(Playlist, playlists_table, properties={
        '_id': playlists_table.c.id,
        '_owner': relationship(User, back_populates='_playlists'),
        '_name': playlists_table.c.name,
        '_episodes': relationship(Episode, secondary=playlist_episodes_table, back_populates='playlists')
    })

