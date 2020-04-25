import gzip
import json

import boto3
from botocore.exceptions import ClientError

from chalice import BadRequestError, Chalice, NotFoundError, Response
from chalicelib.helpers import user
from chalicelib.service.db import base, db

app = Chalice(app_name='test')
app.api.binary_types.append("application/json")
app.debug = True

s3 = boto3.client("s3", region_name="eu-west-2")
bucket = "zappa-portfolio"

base.metadata.create_all(db)

@app.route('/')
def index():
    """
    Just for simple test
    :return:
    """
    return {'hello': 'world'}


@app.route("/users", methods=["GET", "POST"])
def users():
    """
    GET and POST users
    :return:
    """
    request = app.current_request
    if request.method == 'POST':
        return user.add_user(request)
    elif request.method == 'GET':
        pass
        # TODO: implement GET from DB using helper


# These are left here for reference from earlier experiments
@app.route('/ziptest')
def ziptest():
    blob = json.dumps({'hello': 'world'}).encode('utf-8')
    payload = gzip.compress(blob)
    custom_headers = {
        'Content-Type': 'application/json',
        'Content-Encoding': 'gzip'
    }
    return Response(body=payload,
                    status_code=200,
                    headers=custom_headers)


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        s3.put_object(Bucket=bucket, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            return json.loads(response['Body'].read())
        except ClientError:
            raise NotFoundError(key)
