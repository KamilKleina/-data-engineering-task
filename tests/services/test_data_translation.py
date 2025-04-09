"""Services related to data translation."""

import pytest

from de_solution.exceptions import custom_exceptions
from de_solution.models.models import CSVModel
from de_solution.services import data_translation


@pytest.mark.parametrize(
    "csv_model",
    [
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["", "category_2", "", "item_1"],
                ],
            }),
            id="level_1_empty_level_2_filled",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "", "category_3", "item_1"],
                ],
            }),
            id="level_2_empty_level_3_filled",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "category_2", "", "item_1"],
                    ["", "category_3", "", "item_2"],
                ],
            }),
            id="mixed_with_invalid_first_level",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "category_2", "", "item_1"],
                    ["category_1", "", "category_3", "item_2"],
                ],
            }),
            id="mixed_with_invalid_second_level",
        ),
    ],
)
def test_validate_levels_invalid_structure(
    csv_model: CSVModel,
) -> None:
    with pytest.raises(custom_exceptions.InvalidLevelStructureError):
        data_translation.validate_levels(csv_model)


@pytest.mark.parametrize(
    "csv_model",
    [
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "", "", "item_1"],
                ],
            }),
            id="valid_structure_only_level_1_filled",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "subcategory_1", "", "item_1"],
                ],
            }),
            id="valid_structure_level_1_2_filled_level_3_empty",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "subcategory_1", "subsubcategory_1", "item_1"],
                ],
            }),
            id="valid_structure_all_levels_filled",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "subcategory_1", "", "item_1"],
                ],
            }),
            id="valid_structure_level_1_2_filled_level_3_empty_second_row",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "level_3", "item_id"],
                    ["category_1", "subcategory_1", "subsubcategory_1", "item_1"],
                    ["category_2", "subcategory_2", "subsubcategory_2", "item_2"],
                ],
            }),
            id="valid_structure_all_levels_filled_multiple_rows",
        ),
    ],
)
def test_validate_levels_valid_structure(
    csv_model: CSVModel,
) -> None:
    data_translation.validate_levels(csv_model)


@pytest.mark.parametrize(
    ("csv_model", "expected_json"),
    [
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "item_id"],
                    ["A", "1"],
                ],
            }),
            {
                "children": {
                    "A": {
                        "children": {
                            "1": {
                                "item": True,
                            },
                        },
                    },
                },
            },
            id="level_1_case",
        ),
        pytest.param(
            CSVModel.from_data({
                "data": [
                    ["level_1", "level_2", "item_id"],
                    ["category_1", "category_2", "item_1"],
                    ["category_1", "category_3", "item_2"],
                ],
            }),
            {
                "children": {
                    "category_1": {
                        "children": {
                            "category_2": {
                                "children": {
                                    "item_1": {
                                        "item": True,
                                    },
                                },
                            },
                            "category_3": {
                                "children": {
                                    "item_2": {
                                        "item": True,
                                    },
                                },
                            },
                        },
                    },
                },
            },
            id="level_2_case",
        ),
    ],
)
def test_get_json_structure(
    csv_model: CSVModel,
    expected_json: dict[str, dict[str, str]],
) -> None:
    assert data_translation.get_json_structure(csv_model) == expected_json
