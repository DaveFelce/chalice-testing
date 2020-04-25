import factory
import faker
from chalicelib import models
from chalicelib.service.db import db
from factory import lazy_attribute
from sqlalchemy.orm import scoped_session, sessionmaker

fake = faker.Factory.create()


def UserFactory(db_session, **kwargs):
    class _UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = models.User
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        first_name = lazy_attribute(lambda o: fake.name())
        last_name = lazy_attribute(lambda o: fake.name())
        username = lazy_attribute(lambda o: fake.name())

    return _UserFactory

def PostFactory(db_session, **kwargs):
    class _PostFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = models.Post
            sqlalchemy_session = scoped_session(sessionmaker(bind=db))

        headline = lazy_attribute(lambda o: fake.text())
        text = lazy_attribute(lambda o: fake.text())
        user_id = factory.SelfAttribute("user.user_id")
        user = factory.SubFactory(UserFactory)

    return _PostFactory
