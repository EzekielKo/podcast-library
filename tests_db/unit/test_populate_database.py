from sqlalchemy import inspect, select
from podcast.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert set(inspector.get_table_names()) == {'authors', 'podcasts', 'categories', 'podcast_categories', 'episodes', 'users', 'subscriptions', 'reviews', 'playlists', 'playlist_episodes'}

def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]  # Assuming 'authors' is first

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_author_names = []
        for row in result:
            all_author_names.append(row['name'])

        assert all_author_names[0] == 'D Hour Radio Network'
        assert all_author_names[1] == 'Brian Denny'


def test_database_populate_select_all_podcasts(database_engine):
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]  # Assuming 'podcasts' is second

    podcasts_table = metadata.tables[name_of_podcasts_table]

    with database_engine.connect() as connection:
        select_statement = select([podcasts_table])
        result = connection.execute(select_statement)

        all_podcasts = []
        for row in result:
            all_podcasts.append((row['id'], row['title']))

    # Assert that podcasts were returned
    assert len(all_podcasts) > 0, "No podcasts were returned from the database."

    # Assert that each podcast has an id and title
    for podcast in all_podcasts:
        assert podcast[0] is not None, "Podcast ID should not be None."
        assert isinstance(podcast[0], int), "Podcast ID should be an integer."
        assert podcast[1] is not None, "Podcast title should not be None."
        assert isinstance(podcast[1], str), "Podcast title should be a string."


    expected_podcast = (1, "D-Hour Radio Network")
    assert expected_podcast in all_podcasts, f"Expected podcast {expected_podcast} not found."

    expected_count = 1000  # Replace with actual expected count
    assert len(all_podcasts) == expected_count, f"Expected {expected_count} podcasts, but found {len(all_podcasts)}."
