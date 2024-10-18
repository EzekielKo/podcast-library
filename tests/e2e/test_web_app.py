import pytest
from flask import session


def test_register(client):
    # Check that we can retrieve the register page.
    response = client.get('/authentication/register')
    assert response.status_code == 200

    # Test successful registration
    response = client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    assert response.headers['Location'] == '/authentication/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Your user name is required'),
    ('ab', 'password', b'Your user name is too short'),
    ('newuser', '', b'Your password is required'),
    ('newuser', 'password', b'Your password must'),
    ('takenuser', 'Password123!', b'Your user name is already taken - please supply another')
))
def test_register_with_invalid_input(client, user_name, password, message):
    client.post(
        '/authentication/register',
        data={'user_name': "takenuser", 'password': password}
    )
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    # Check if the error message is somewhere in the HTML response
    assert message in response.data, f"Expected error message '{message.decode()}' not found in response."



def test_login(client, auth):
    # Register the user first
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )

    # Now test login
    response = auth.login()
    assert response.status_code == 302  # Expect redirect to home
    # Check for relative URL since Flask provides '/' instead of 'http://localhost/'
    assert response.headers['Location'] == "/"


def test_logout(client, auth):
    # First log the user in
    auth.login()

    # Now test logout
    with client:
        auth.logout()
        assert 'user_name' not in session

def test_review_on_podcast(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    # Login a user first
    auth.login(user_name='newuser', password='Password123!')

    # Get the podcast description page (to get the form)
    response = client.get('/description/1')  # Assuming podcast_id=1 exists
    assert response.status_code == 200

    # Submit a valid review
    response = client.post(
        '/review',
        data={
            'comment': 'Great podcast!',
            'rating': 5,
            'podcast_id': 1  # Assuming podcast_id=1
        }
    )
    assert response.status_code == 302  # Expect a redirect after successful submission
    assert response.headers['Location'] == '/description/1'

@pytest.mark.parametrize(('comment', 'rating', 'messages'), (
    ('', 5, (b'Your comment is too short')),  # Empty comment
    ('Good', 0, (b'Rating must be between 1 and 5')),  # Invalid rating
    ('Nice', 6, (b'Rating must be between 1 and 5')),  # Invalid rating
))
def test_review_with_invalid_input(client, auth, comment, rating, messages):
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    # Login a user first
    auth.login(user_name='newuser', password='Password123!')

    # Submit an invalid review
    response = client.post(
        '/review',
        data={
            'comment': comment,
            'rating': rating,
            'podcast_id': 1  # Assuming podcast_id=1
        }
    )
    # Check that supplying invalid data generates appropriate error messages
    for message in messages:
        assert message in response.data

def test_add_to_playlist(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    # Login a user first
    auth.login(user_name='newuser', password='Password123!')

    # Add an episode to the playlist
    response = client.post('/add_to_playlist/1/1')
    assert response.status_code == 302
    assert response.headers['Location'] == '/description/1?rendered_by_catalogue=False'

def test_remove_from_playlist(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    # Login a user first
    auth.login(user_name='newuser', password='Password123!')
    response = client.post('/add_to_playlist/1/1')
    # Remove an episode from the playlist
    response = client.post('/remove/1')  # Assuming episode_id=1 exists in the user's playlist
    assert response.status_code == 302  # Expect a redirect back to the playlist page
    assert response.headers['Location'] == '/playlist'

def test_view_playlist(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'newuser', 'password': 'Password123!'}
    )
    # Login a user first
    auth.login(user_name='newuser', password='Password123!')

    # Get the playlist page
    response = client.get('/playlist')
    assert response.status_code == 200
    assert b"My Playlist" in response.data

def test_login_required_to_review(client):
    # Try to access the review page without logging in
    response = client.get('/review?podcast=1')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_login_required_to_add_to_playlist(client):
    # Try to add an episode to the playlist without logging in
    response = client.post('/add_to_playlist/1/1')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'
