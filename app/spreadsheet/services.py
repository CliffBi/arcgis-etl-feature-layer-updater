import json
import logging
from abc import ABC

import pandas as pd

from app.spreadsheet.exceptions import SheetSchemaMismatchError
from app.settings import SHEET_FORMAT_PATH, SHEET_FORMAT_BY_GID_PATH
from app.spreadsheet.provider import AbsSpreadsheetProvider

logger = logging.getLogger(__name__)


class AbsSpreadsheetService(ABC):
    """
    Abstract base class containing service logic between the spreadsheet provider API and project business logic.

    Example usage: fetching data from sheet configuration files and matching proper columns for provider layer.
    """
    sheet_format_path: str

    def __init__(self, provider: AbsSpreadsheetProvider) -> None:
        self.provider = provider

        self._sheet_formats = dict()

    @property
    def sheet_formats(self):
        if not self._sheet_formats:
            with open(self.sheet_format_path) as f:
                self._sheet_formats = json.load(f)
        return self._sheet_formats

    def read_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        """
        Method reads sheet data from provided spreadsheet or specific sheet.
        Raises ValueError if spreadsheet or sheet wasn't found in sheet and format config files.
        If columns different from config file, method raises ValueError exception.
        """
        if sheet_name not in self.sheet_formats:
            msg = f"{sheet_name} doesnt' exist in sheet_format config file."
            logger.error(msg)
            raise KeyError(msg)

        data = self.provider.get_sheet_data(spreadsheet_id, sheet_name)
        sheet_format = self.sheet_formats[sheet_name]

        expected_column_names = list(sheet_format.values())

        if list(data.columns) != expected_column_names:
            missing = set(expected_column_names) - set(data.columns)
            extra = set(data.columns) - set(expected_column_names)
            msg = f"Columns mismatch! Missing: {missing}, Extra: {extra}"
            logger.error(msg)
            raise SheetSchemaMismatchError(msg)

        return data


class SpreadsheetService(AbsSpreadsheetService):
    """
    Service class for spreadsheet interaction using sheet names.
    Loads sheet format from default SHEET_FORMAT_PATH.
    """
    def __init__(self, **kwargs):
        self.sheet_format_path = SHEET_FORMAT_PATH
        super().__init__(**kwargs)


class GidSpreadsheetService(AbsSpreadsheetService):
    """
    Service class for spreadsheet interaction using sheet GID.
    Loads sheet format from SHEET_FORMAT_BY_GID_PATH.
    """
    def __init__(self, **kwargs):
        self.sheet_format_path = SHEET_FORMAT_BY_GID_PATH
        super().__init__(**kwargs)
