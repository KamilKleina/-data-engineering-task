"""Tests for data translation."""

import csv
import json
import typing as t
from http import HTTPStatus
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from de_solution.main import app

TEST_DATA_DIR: t.Final[Path] = Path("tests/test_data")
client = TestClient(app)


def read_csv_for_api(path: Path) -> list[list[str]]:
    """Read csv file to accepted by API format."""
    with path.open() as file:
        return list(csv.reader(file))


def read_expected_json(path: Path) -> dict[str, t.Any]:
    """Read json file."""
    with path.open() as file:
        return json.load(file)


def test_get_json_structure_empty_csv() -> None:
    """Test the CSV to JSON conversion endpoint - empty csv."""
    response = client.post(
        "",
        json={"data": []},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert "CSVFormatError" in response.json()


def test_get_json_structure_different_column_length() -> None:
    """Test the CSV to JSON conversion endpoint - different column length."""
    response = client.post(
        "",
        json={
            "data": [
                [
                    "level_1",
                    "level_2",
                ],
                [
                    "category_1",
                    "",
                    "item_1",
                ],
                [
                    "category_2",
                    "category_3",
                    "item_2",
                ],
            ],
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert "CSVFormatError" in response.json()


def test_get_json_structure_basic_case() -> None:
    """Test the CSV to JSON conversion endpoint."""
    response = client.post(
        "",
        json={
            "data": [
                [
                    "level_1",
                    "level_2",
                    "item_id",
                ],
                [
                    "category_1",
                    "category_2",
                    "item_1",
                ],
                [
                    "category_1",
                    "category_3",
                    "item_2",
                ],
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
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
    }


def test_get_json_structure_small_data_case() -> None:
    """Test the CSV to JSON conversion endpoint."""
    response = client.post(
        "",
        json={
            "data": [
                [
                    "level_1",
                    "level_2",
                    "item_id",
                ],
                [
                    "category_1",
                    "category_2",
                    "item_1",
                ],
                [
                    "category_1",
                    "category_3",
                    "item_2",
                ],
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {
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
    }


@pytest.mark.parametrize(
    ("input_file", "output_file"),
    [
        ("small_input.csv", "small_output.json"),
        ("large_input.csv", "large_output.json"),
    ],
)
def test_csv_to_json(input_file: str, output_file: str) -> None:
    input_path = TEST_DATA_DIR / input_file
    output_path = TEST_DATA_DIR / output_file

    csv_data = read_csv_for_api(input_path)
    expected_json = read_expected_json(output_path)

    response = client.post("", json={"data": csv_data})

    assert response.status_code == 200
    assert response.json() == expected_json
