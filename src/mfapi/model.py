"""
Pydantic models for the mutual fund API responses.

This module defines models that map to the following schemas:
- SchemeSearchResult
- SchemeListItem
- NAVData
- SchemeMeta
- NAVHistoryResponse
- LatestNAVItem

Each model includes descriptive Field metadata and supports population
by both field name and alias (useful when parsing API responses
that use camelCase or other naming conventions).
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class MFBaseModel(BaseModel):
    """
    Base model with common configuration for all API models.
    - allow_population_by_field_name: allow constructing models using Pythonic field names.
    - use_enum_values: serialize enums to their values by default.
    - anystr_strip_whitespace: strip whitespace from string fields.
    """

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        anystr_strip_whitespace = True
        orm_mode = True


class SchemeSearchResult(MFBaseModel):
    """
    Minimal search result for a scheme.
    """

    scheme_code: int = Field(
        ..., alias="schemeCode", description="Unique identifier for the scheme"
    )
    scheme_name: str = Field(
        ..., alias="schemeName", description="Full name of the mutual fund scheme"
    )


class SchemeListItem(MFBaseModel):
    """
    Item in a list of schemes returned by list endpoints.
    """

    scheme_code: int = Field(
        ..., alias="schemeCode", description="Unique identifier for the scheme"
    )
    scheme_name: str = Field(
        ..., alias="schemeName", description="Full name of the mutual fund scheme"
    )
    isin_growth: Optional[str] = Field(
        None, alias="isinGrowth", description="ISIN code for growth option (nullable)"
    )
    isin_div_reinvestment: Optional[str] = Field(
        None,
        alias="isinDivReinvestment",
        description="ISIN code for dividend reinvestment option (nullable)",
    )


class NAVData(MFBaseModel):
    """
    Single NAV entry for a given date.
    - `date` is expected in DD-MM-YYYY format.
    - `nav` is a string representing the NAV with 5 decimal precision (e.g. '1234.56789').
    """

    date: str = Field(..., description="Date in DD-MM-YYYY format")
    nav: str = Field(..., description="Net Asset Value with 5 decimal precision")


class SchemeMeta(MFBaseModel):
    """
    Metadata describing a scheme. Field names here use snake_case aliases
    to match the provided schema.
    """

    fund_house: Optional[str] = Field(
        None, alias="fund_house", description="Name of the fund house"
    )
    scheme_type: Optional[str] = Field(
        None,
        alias="scheme_type",
        description="Type of the scheme (e.g., Open Ended Schemes)",
    )
    scheme_category: Optional[str] = Field(
        None, alias="scheme_category", description="Category of the scheme"
    )
    scheme_code: int = Field(
        ..., alias="scheme_code", description="Unique identifier for the scheme"
    )
    scheme_name: str = Field(
        ..., alias="scheme_name", description="Full name of the mutual fund scheme"
    )
    isin_growth: Optional[str] = Field(
        None, alias="isin_growth", description="ISIN code for growth option (nullable)"
    )
    isin_div_reinvestment: Optional[str] = Field(
        None,
        alias="isin_div_reinvestment",
        description="ISIN code for dividend reinvestment option (nullable)",
    )


class NAVHistoryStatus(str, Enum):
    """
    Allowed values for response status in NAVHistoryResponse.
    """

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class NAVHistoryResponse(MFBaseModel):
    """
    Response wrapper for NAV history endpoints.
    - `meta` contains scheme-level metadata.
    - `data` is an ordered list of NAVData items.
    - `status` indicates whether the response was successful.
    """

    meta: SchemeMeta = Field(..., description="Metadata for the scheme")
    data: List[NAVData] = Field(..., description="List of NAV data points")
    status: NAVHistoryStatus = Field(
        ..., description="Response status (SUCCESS or ERROR)"
    )


class LatestNAVItem(MFBaseModel):
    """
    Model describing the latest NAV item for a scheme.
    Field aliases follow camelCase to match typical JSON responses.
    """

    scheme_code: int = Field(
        ..., alias="schemeCode", description="Unique identifier for the scheme"
    )
    scheme_name: str = Field(
        ..., alias="schemeName", description="Full name of the mutual fund scheme"
    )
    fund_house: Optional[str] = Field(
        None, alias="fundHouse", description="Name of the fund house"
    )
    scheme_type: Optional[str] = Field(
        None,
        alias="schemeType",
        description="Type of the scheme (e.g., Open Ended Schemes)",
    )
    scheme_category: Optional[str] = Field(
        None, alias="schemeCategory", description="Category of the scheme"
    )
    isin_growth: Optional[str] = Field(
        None, alias="isinGrowth", description="ISIN code for growth option (nullable)"
    )
    isin_div_reinvestment: Optional[str] = Field(
        None,
        alias="isinDivReinvestment",
        description="ISIN code for dividend reinvestment option (nullable)",
    )
    nav: str = Field(
        ..., alias="nav", description="Latest Net Asset Value with 5 decimal precision"
    )
    date: str = Field(..., alias="date", description="NAV date in DD-MM-YYYY format")


__all__ = [
    "MFBaseModel",
    "SchemeSearchResult",
    "SchemeListItem",
    "NAVData",
    "SchemeMeta",
    "NAVHistoryStatus",
    "NAVHistoryResponse",
    "LatestNAVItem",
]
