import pytest

from app import app
from chalicelib.models import base
from chalicelib.service.db import db
from sqlalchemy.orm import scoped_session, sessionmaker


# Fixtures
@pytest.fixture(scope="session")
def db_session():
    db_session = scoped_session(sessionmaker(bind=db))
    yield db_session
    db_session.remove()


@pytest.fixture(scope="module", autouse=True)
def setup_db(db_session):
    """
    autouse set to True so will be run before each test function, to set up tables
    and tear them down after each test runs

    :return:
    """
    base.metadata.create_all(db_session.bind.engine)

    yield  # Nothing to yield, this fixture just sets up and destroys tables

    # Don't commit anything to the actual DB
    db_session.rollback()
    # Drop all tables after each test
    base.metadata.drop_all(db_session.bind.engine)


@pytest.fixture
def gateway_factory():
    """
    Use LocalGateway to test the API - like Flask's test client, kind of
    """
    from chalice.config import Config
    from chalice.local import LocalGateway

    def create_gateway(config=None):
        if config is None:
            config = Config()
        return LocalGateway(app, config)

    return create_gateway
