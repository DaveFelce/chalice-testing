from contextlib import contextmanager

from chalicelib.service.db import db
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=db)()


@contextmanager
def get_session():
    """
    Get a SQLA session
    :return: a session obj
    """
    yield session
