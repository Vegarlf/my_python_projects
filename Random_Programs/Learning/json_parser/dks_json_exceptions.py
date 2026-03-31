"""Special JSON Exceptions and Errors For The JSON Parser.

Structure:
=========
JSONException - Base Class For All Errors
|- JSONStructureError - Base Class For Structure Errors In JSON File
|    |- JSONArrayStructureError - Invalid Array Object
|    |- JSONObjectStructureError - Invalid Object Object
|    |- JSONTrailingCommaError - Trailing Comma Error
|    `-- JSONUnterminatedStringError - Unterminated String
`--JSONEOFError - JSON End Of File Error, Unexpected End Of File
"""

# New exceptions will be added here as the parser is built and I encounter new error cases.
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class JSONException(ValueError, ABC):
    """Base Class For Special JSON Exceptions. CANNOT BE INSTANTIATED DIRECTLY.

    Inherits From ValueError.
    self.doc can be raw source text, context is generated automatically.
    self.doc treats "" differently from None, "" is an empty document, while None (default) is no document provided.
    self.pos is index where error occurred.
    negative self.pos is allowed for indexing from end, it gets converted to positive index.
    """

    doc: Optional[str] = None
    pos: Optional[int] = None

    def __post_init__(self):
        if self.doc is None and self.pos is not None:
            logger.warning("attempted to provide position without providing document")
            raise ValueError(
                f"Provided position to {self.__class__.__name__} without providing document."
            )
        if self.pos is not None and self.pos not in range(
            (-len(self.doc)), len(self.doc)
        ):
            logger.error("Position Provided To Exception Not In Document Provided.")
            raise IndexError("Position Index Out Of Bounds.")

    @property
    def positive_pos_converter(self) -> Optional[int]:
        """Generates positive pos (index) from negative one."""
        if self.pos is None:
            return None
        if self.pos < 0:
            return len(self.doc) + self.pos
        return self.pos

    @property
    def context_snippet(self) -> Optional[str]:
        """Generates context from document and position"""
        actual_pos: Optional[int] = self.positive_pos_converter
        context: Optional[str] = (
            self.doc[max(0, actual_pos - 10) : min(len(self.doc), actual_pos + 10)]
            if self.doc is not None and self.pos is not None
            else None
        )
        return context

    @abstractmethod
    def __str__(self):
        """Force Subclasses To Implement Custom Error Printing."""
        actual_pos: int = self.positive_pos_converter
        location_string = (
            f"at index {actual_pos}"
            if actual_pos is not None
            else "~no location_string provided~"
        )
        context: Optional[str] = self.context_snippet
        source_doc_string = (
            f"in document context {context}"
            if context is not None
            else "~no source_doc_string provided~"
        )
        return f"JSONError {location_string} {source_doc_string}"

    @classmethod
    def verify(cls, condition: bool, **kwargs) -> None:
        """Verifies If Condition, Else Raises Error From Which Method Is Called."""
        if cls is JSONException:
            logger.error(f"Called Base Exception {cls.__name__} Directly.")
            raise TypeError(f"{cls.__name__} Cannot Be Used Directly. Use A Subclass.")
        if not condition:
            exc = cls(**kwargs)
            logger.error(f"Raised JSON Exception {cls.__name__} Through verify().")
            raise exc


@dataclass(frozen=True, kw_only=True)
class JSONStructureError(JSONException):
    """Exception Raised When JSON Structure Is Deemed Invalid."""

    char: Optional[str] = None

    def __str__(self):
        base_string = super().__str__()
        character_string = (
            f"received {self.char}"
            if self.char is not None
            else "~no character_string provided~"
        )
        return f"{self.__class__.__name__}, {base_string}, {character_string}"


@dataclass(frozen=True, kw_only=True)
class JSONArrayStructureError(JSONStructureError):
    """Exception Raised When Invalid Array Object Is Found."""


@dataclass(frozen=True, kw_only=True)
class JSONObjectStructureError(JSONStructureError):
    """Exception Raised When Invalid Object Is Found."""


@dataclass(frozen=True, kw_only=True)
class JSONEOFError(JSONException):
    """Exception Raised When EOF Is Different From Expected."""

    received: Optional[str] = None
    expected: Optional[str] = None

    def __str__(self):
        base_string = super().__str__()
        received_string = (
            f"received {self.received}"
            if self.received is not None
            else "~no received_string provided~"
        )
        expected_string = (
            f"expected {self.expected}"
            if self.expected is not None
            else "~no expected_string provided~"
        )
        return f"{self.__class__.__name__}, {base_string}, {expected_string}, {received_string}"


@dataclass(frozen=True, kw_only=True)
class JSONUnterminatedStringError(JSONStructureError):
    """Exception Raised When Parser Encounters An Unterminated String."""


@dataclass(frozen=True, kw_only=True)
class JSONTrailingCommaError(JSONStructureError):
    """Exception Raised When Parser Encounters A Trailing Comma."""
