import json
import base64
import os
from jsonschema import ValidationError
import boto3
from botocore.exceptions import ClientError
import slugid
import liburtask

# initialize s3 client
s3 = boto3.client("s3")

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
    # generate json document for new board
    new_board_json = json.dumps(liburtask.NEW_BOARD_TEMPLATE)

    # generate an id for the new board
    new_board_id = slugid.generate_slugid()
    new_board_key = f"{new_board_id}.json"  # s3 storage key for this board

    # store the object in s3
    s3.put_object(
        Bucket=BOARDS_BUCKET_NAME,
        Key=new_board_key,
        Body=new_board_json.encode("utf-8"),
    )

    # return id of the created board
    body = {"id": new_board_id}

    return {
        "statusCode": 201,  # HTTP 201 - created
        "body": json.dumps(body),
    }


def update_board(event, context):
    board_id = event["pathParameters"]["board_id"]  # board id to PUT
    req_body = _get_body(event)  # body associated with the request

    # check that the body is valid
    try:
        # validate the board
        liburtask.validate(req_body)
    except ValidationError as e:
        # return the validation error
        resp_body = {"message": str(e)}

        return {"statusCode": 400, "body": json.dumps(resp_body)}

    # check that the id we are writing to is valid
    if not slugid.is_valid_slugid(board_id):
        resp_body = {"message": f"Invalid board ID '{board_id}'"}
        return {"statusCode": 400, "body": json.dumps(resp_body)}

    board_key = f"{board_id}.json"  # s3 storage key for this board

    s3.put_object(
        Bucket=BOARDS_BUCKET_NAME,
        Key=board_key,
        Body=json.dumps(req_body).encode("utf-8"),
    )

    return {"statusCode": 200}


def get_board(event, context):
    board_id = event["pathParameters"]["board_id"]

    # check that the board id is valid
    if not slugid.is_valid_slugid(board_id):
        resp_body = {"message": f"Invalid board ID '{board_id}'"}
        return {"statusCode": 400, "body": json.dumps(resp_body)}

    board_key = f"{board_id}.json"  # s3 storage key for this board

    try:
        # get board object from s3
        s3_resp = s3.get_object(
            Bucket=BOARDS_BUCKET_NAME,
            Key=board_key,
        )
    except ClientError as e:
        # error getting from S3
        status_code = 500
        message = ""

        if e.response["Error"]["Code"] == "NoSuchKey":
            # object doesn't exist
            status_code = 404
            message = "Board does not exist."
        else:
            raise e

        resp_body = {"message": message}

        return {"statusCode": status_code, "body": json.dumps(resp_body)}

    board_body = s3_resp["Body"].read().decode("utf-8")

    return {"statusCode": 200, "body": board_body}


def delete_board(event, context):
    board_id = event["pathParameters"]["board_id"]

    # check that the board id is valid
    if not slugid.is_valid_slugid(board_id):
        resp_body = {"message": f"Invalid board ID '{board_id}'"}
        return {"statusCode": 400, "body": json.dumps(resp_body)}

    board_key = f"{board_id}.json"  # s3 storage key for this board

    try:
        # delete board object from s3
        s3.delete_object(
            Bucket=BOARDS_BUCKET_NAME,
            Key=board_key,
        )
    except ClientError as e:
        # error getting from S3
        status_code = 500
        message = ""

        if e.response["Error"]["Code"] == "NoSuchKey":
            # object doesn't exist
            status_code = 404
            message = "Board does not exist."
        else:
            raise e

        resp_body = {"message": message}

        return {"statusCode": status_code, "body": json.dumps(resp_body)}

    return {"statusCode": 204}
