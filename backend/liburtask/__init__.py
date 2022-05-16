"""Backend library for urtask.
"""
from liburtask.validate import validate

NEW_BOARD_TEMPLATE = {
    "name": "Tasks",
    "lists": [
        {"name": "To-do", "tasks": [{"body": "Start keeping track of tasks!"}]},
        {"name": "In progress", "tasks": []},
        {"name": "Done", "tasks": [{"body": "Setup urtask"}]},
    ],
}
"""Template for newly created boards.
"""

# validate the template
# this will raise ValidationError on import if the default board is somehow invalid
validate(NEW_BOARD_TEMPLATE)
