import pytest

from rest_api.app import create_app


@pytest.fixture
def app(tmp_path):
    database = tmp_path / "users.db"
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}",
    })
    yield application
