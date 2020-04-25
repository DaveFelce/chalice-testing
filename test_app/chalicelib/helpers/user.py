from chalice import BadRequestError
from chalicelib.models import User
from chalicelib.utils import get_session


def add_user(request):
    """
    Function to add a User
    :param request: The incoming request to the API
    """
    try:
        first_name = request.json_body['first_name']
        last_name = request.json_body['last_name']
        username = request.json_body['username']

        with get_session() as session:
            new_user = User(first_name=first_name, last_name=last_name, username=username)

            session.add(new_user)
            session.commit()

            return
    except Exception as e:
        raise BadRequestError(e)
