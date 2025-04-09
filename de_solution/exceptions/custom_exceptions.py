"""Custom exceptions."""

import typing as t
from dataclasses import dataclass


@dataclass
class RowFormatError(Exception):
    """Exception raised for errors in the Row format."""

    message: str

    @t.override
    def __str__(self) -> str:
        """Return a string representation of the error."""
        return f"CSVFormatError: {self.message}"


@dataclass
class CSVFormatError(Exception):
    """Exception raised for errors in the CSV format."""

    message: str

    @t.override
    def __str__(self) -> str:
        """Return a string representation of the error."""
        return f"CSVFormatError: {self.message}"


@dataclass
class InvalidLevelStructureError(Exception):
    """Exception raised for errors in the CSV Hierarchy."""

    message: str

    @t.override
    def __str__(self) -> str:
        """Return a string representation of the error."""
        return f"InvalidLevelStructureError: {self.message}"
