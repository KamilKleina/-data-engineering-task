"""Services related to data translation."""

from de_solution.exceptions import custom_exceptions
from de_solution.models.models import CSVModel


def validate_levels(
    csv_model: CSVModel,
) -> None:
    """Validate structure of levels."""
    for row in csv_model.rows:
        for level in range(1, 3):
            current_level = getattr(row, f"level_{level}", None)
            next_level = getattr(row, f"level_{level + 1}", None)

            if current_level or not next_level:
                continue

            raise custom_exceptions.InvalidLevelStructureError(
                message=(
                    f"Invalid structure: {level=} is empty but {level + 1=} is not."
                ),
            )


def get_json_structure(csv_model: CSVModel) -> dict[str, dict[str, str]]:
    """Get json structure."""
    json_structure: dict[str, dict[str, str]] = {"children": {}}
    for row in csv_model.rows:
        levels: list[str] = []
        for level in range(1, 4):
            level_value: str | None = getattr(row, f"level_{level}", None)

            if not level_value:
                break

            levels.append(level_value)

        current = json_structure["children"]
        for level in levels:
            if level not in current:
                current[level] = {"children": {}}
            current = current[level]["children"]

        current[row.item_id] = {"item": True}

    return json_structure
