from abc import ABC

import pandas as pd

from app.spreadsheet.services import AbsSpreadsheetService


class AbsSpreadsheetConnector(ABC):
    def __init__(self, spreadsheet_id: str, spreadsheet_service: AbsSpreadsheetService):
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheet_service = spreadsheet_service


class SpreadsheetConnector(AbsSpreadsheetConnector):
    """
    Current class is responsible for gathering information from 'Вихідні дані' file.
    """
    def __init__(self, **kwargs):
        self._data_sheet = pd.DataFrame()
        super().__init__(**kwargs)

    @property
    def data_sheet(self):
        if self._data_sheet.empty:
            self._data_sheet = self.spreadsheet_service.read_sheet_data(
                self.spreadsheet_id, "Дані"
            )
        return self._data_sheet


class GidSpreadsheetConnector(AbsSpreadsheetConnector):
    """
    Current class is responsible for gathering information from 'Вихідні дані' file.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._zero_sheet = pd.DataFrame()

    @property
    def zero_sheet(self):
        if self._zero_sheet.empty:
            self._zero_sheet = self.spreadsheet_service.read_sheet_data(
                self.spreadsheet_id, "0"
            )
        return self._zero_sheet
