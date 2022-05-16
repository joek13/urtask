"""Tools for generating UUID slugs, which are used as board IDs.
"""

import binascii
import uuid
import base64


def generate_slugid() -> str:
    """Generates a UUID slug.

    A UUID slug is a URL-safe base64-encoded UUID with trailing '=' and newlines removed.
    Uses Python's `uuid` library to generate UUIDs.

    Returns:
        str: Generated UUID slug.
    """
    object_uuid = uuid.uuid4()
    b64_encoded = base64.urlsafe_b64encode(object_uuid.bytes)
    return b64_encoded.decode("utf-8").rstrip("=\n")


def is_valid_slugid(slugid: str) -> bool:
    """Checks whether a given string represents a valid UUID slug.

    Args:
        slugid (str): String to validate.

    Returns:
        bool: Whether the argument is a valid UUID slug.
    """

    try:
        # decode slug
        # need to add padding for base64 decode to work properly
        # (since we truncate it in generate_slugid)
        # luckily, python is able to handle extra padding no problem
        # so if we add 2 chars of padding -- the maximum amount -- we'll be fine
        # see: https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding

        decoded = base64.urlsafe_b64decode(slugid + "==")

        # convert to UUID
        _ = uuid.UUID(bytes=decoded)
        return True
    except (ValueError, binascii.Error) as e:
        return False
