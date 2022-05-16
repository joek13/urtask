"""Validation logic for urtask boards.
"""
import jsonschema
import json
from pathlib import Path

# get path to sibling board.schema.json
_board_schema_path = Path.joinpath(Path(__file__).parent.resolve(), "board.schema.json")

# open the board schema and load into Python object
with open(_board_schema_path, "r") as f:
    _schema = json.loads(f.read())


def validate(board: dict):
    """Validates a board dict.

    Ensures the board dict conforms to a given JSON Schema.

    Args:
        board (dict): Python dict to validate. Perhaps loaded from JSON.

    Returns:
        None

    Throws:
        Throws ValidationError if board fails to validate.
    """
    jsonschema.validate(instance=board, schema=_schema)
