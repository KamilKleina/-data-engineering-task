"""API."""

import typing as t

from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from de_solution.exceptions import custom_exceptions
from de_solution.middlewares import logging_middleware
from de_solution.models.models import CSVModel
from de_solution.services import data_translation as data_translation_service

app = FastAPI(
    root_path="",
    title="Data Engineering Solution",
)
app.add_middleware(logging_middleware.RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/",
    response_model=dict[str, t.Any],
    summary="Convert CSV to JSON",
    description="Endpoint converts CSV data to JSON format according to the rules.",
)
def get_json_structure(
    csv_data: t.Annotated[
        dict[str, list[list[str]]],
        Body(
            examples=[
                {
                    "data": [
                        ["level_1", "level_2", "level_3", "item_id"],
                        ["category_1", "subcategory_1", "subsubcategory_1", "item_1"],
                        ["category_2", "subcategory_2", "subsubcategory_2", "item_2"],
                    ],
                },
            ],
        ),
    ],
) -> dict[str, t.Any]:
    """Get json structure from csv data."""
    logger.info("Converting CSV to JSON")
    csv_model = CSVModel.from_data(csv_data)
    data_translation_service.validate_levels(csv_model)
    return data_translation_service.get_json_structure(csv_model)


@app.exception_handler(custom_exceptions.CSVFormatError)
def csv_format_error_handler(
    _: Request,
    exc: custom_exceptions.CSVFormatError,
) -> JSONResponse:
    """Handle CSV format errors."""
    return JSONResponse(status_code=400, content=f"{exc}")


@app.exception_handler(custom_exceptions.InvalidLevelStructureError)
def csv_level_structure_error_handler(
    _: Request,
    exc: custom_exceptions.InvalidLevelStructureError,
) -> JSONResponse:
    """Handle CSV Invalid Level Structure errors."""
    return JSONResponse(status_code=400, content=f"{exc}")
