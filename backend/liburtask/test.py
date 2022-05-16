import unittest

from jsonschema import ValidationError
import validate


class TestValidation(unittest.TestCase):
    def test_valid_object(self):
        # valid task board
        valid_object = {
            "name": "tasks",
            "lists": [
                {"name": "To-Do", "tasks": [{"body": "My first task"}]},
                {"name": "In Progress", "tasks": []},
                {"name": "Done", "tasks": []},
            ],
        }

        try:
            validate.validate(valid_object)
        except ValidationError:
            self.fail("Valid board failed to validate")

    def test_invalid_object(self):
        # invalid task board - name must be a string
        invalid_object = {
            "name": 123,
            "lists": [
                {"name": "To-Do", "tasks": [{"body": "My first task"}]},
                {"name": "In Progress", "tasks": []},
                {"name": "Done", "tasks": []},
            ],
        }

        with self.assertRaises(ValidationError):
            validate.validate(invalid_object)
