import os

# Settings are read from the environment when the app is imported. Point them
# at SQLite so the suite can never touch a real MySQL database.
os.environ["APP_SECRET_KEY"] = "test"
os.environ["APP_CORS_ORIGINS"] = "http://localhost:3000"
os.environ["APP_DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import application
from db.connection import get_session
from db.models import Base


@pytest.fixture
def db():
    """A fresh in-memory database per test."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False)
    engine.dispose()


@pytest.fixture
def client(db):
    def get_test_session():
        with db() as session:
            yield session

    application.dependency_overrides[get_session] = get_test_session
    with TestClient(application) as test_client:
        yield test_client
    application.dependency_overrides.clear()
