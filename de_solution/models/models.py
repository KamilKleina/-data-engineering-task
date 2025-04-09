"""Models."""

import typing as t

from pydantic import BaseModel

from de_solution.exceptions import custom_exceptions


class RowModel(BaseModel):
    """Row model for CSV data."""

    level_1: str
    level_2: str | None = None
    level_3: str | None = None
    item_id: str

    @classmethod
    def from_list(cls, row: list[str]) -> t.Self:
        """Create based on list."""
        match row:
            case [l1, l2, l3, item_id]:
                return cls(level_1=l1, level_2=l2, level_3=l3, item_id=item_id)
            case [l1, l2, item_id]:
                return cls(level_1=l1, level_2=l2, item_id=item_id)
            case [l1, item_id]:
                return cls(level_1=l1, item_id=item_id)
            case _:
                msg = f"Unsupported row format: {row}"
                raise custom_exceptions.RowFormatError(msg)


class CSVModel(BaseModel):
    """Model for CSV data."""

    headers: RowModel
    rows: list[RowModel]

    @classmethod
    def from_data(cls, data: dict[str, list[list[str]]]) -> t.Self:
        """Validate CSV data format."""
        csv_rows = data["data"]
        if not csv_rows:
            msg = "CSV data cannot be empty."
            raise custom_exceptions.CSVFormatError(msg)

        col_count = len(csv_rows[0])
        for row in csv_rows:
            if len(row) != col_count:
                msg = "All rows must have the same number of columns."
                raise custom_exceptions.CSVFormatError(msg)
        headers = RowModel.from_list(csv_rows[0])
        data_rows = [RowModel.from_list(row) for row in csv_rows[1:]]

        return cls(headers=headers, rows=data_rows)
