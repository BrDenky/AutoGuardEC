import pytest
from app import create_app
from config import config

@pytest.fixture
def app():
    app = create_app('development')
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
