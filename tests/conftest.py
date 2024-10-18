import pytest

from podcast import create_app
from podcast.adapters.memoryRepository import MemoryRepository, populate
from utils import get_project_root

# the csv files in the test folder are different from the csv files in the podcast/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()  # Use MemoryRepository or equivalent in your project
    populate(repo, TEST_DATA_PATH)  # Make sure to populate it with test data
    return repo

@pytest.fixture
def client(in_memory_repo):
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })  # Pass the in-memory repo to the app

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='newuser', password='Password123!'):
        return self.__client.post(
            '/authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
