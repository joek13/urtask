import json
import base64
import os

# name of the s3 bucket we store boards in
BOARDS_BUCKET_NAME = os.environ.get("BOARDS_BUCKET_NAME")

# raise error if missing
if BOARDS_BUCKET_NAME is None:
    raise RuntimeError("Missing required environment variable 'BOARDS_BUCKET_NAME'")


def _get_body(event):
    """Gets request body, base64 decodes if necessary,
    and parses JSON into a Python dict.
    """
    # get POST body as a string
    body = event["body"]

    # check if the POST body string is base64-encoded
    if event["isBase64Encoded"]:
        # decode it
        body = base64.b64decode(body)

    # parse into a python object
    return json.loads(body)


def create_board(event, context):
    body = {"hello": "world"}
    return {"statusCode": 200, "body": json.dumps(body)}


def update_board(event, context):
    board_id = event["pathParameters"]["board_id"]
    body = {"hello": "world", "board_id": board_id}
    return {"statusCode": 200, "body": json.dumps(body)}


def get_board(event, context):
    board_id = event["pathParameters"]["board_id"]
    body = {"hello": "world", "board_id": board_id}
    return {"statusCode": 200, "body": json.dumps(body)}


def delete_board(event, context):
    board_id = event["pathParameters"]["board_id"]
    body = {"hello": "world", "board_id": board_id}
    return {"statusCode": 200, "body": json.dumps(body)}
