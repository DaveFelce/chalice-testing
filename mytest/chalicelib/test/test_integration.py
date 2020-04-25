import json
from http import HTTPStatus

from chalicelib import models
from chalicelib.test import factories


class TestMyTest:

    def test_inserts_user_record(self, db_session):
        """
        Basic test to check that it's possible to insert a User record into the DB using a factory
        :param db_session: DB session fixture
        """
        # Given
        first_name = "Hank"

        # When
        new_user = factories.UserFactory(db_session).create(
            **{
                "first_name": first_name
            }
        )
        # Get the resulting record
        rec = (
            db_session.query(models.User)
                .filter(models.User.first_name == first_name)
                .first()
        )

        # Then
        # Check record has been created OK
        assert new_user.first_name == rec.first_name
        assert new_user.user_id == rec.user_id

    def test_index(self, gateway_factory):
        """
        Basic test of the API
        :param gateway_factory: a local gateway fixture
        """
        gateway = gateway_factory()
        response = gateway.handle_request(method="GET",
                                          path="/",
                                          headers={"Accept": "application/json"},
                                          body="")
        assert response["statusCode"] == HTTPStatus.OK
        assert json.loads(response["body"]) == dict([("hello", "world")])
