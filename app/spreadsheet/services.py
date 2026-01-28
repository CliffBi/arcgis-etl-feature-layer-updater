import json
from abc import ABC

from app.exceptions import SheetSchemaMismatchError
from app.settings import SHEET_FORMAT_PATH, SHEET_FORMAT_BY_GID_PATH
from app.spreadsheet.provider import AbsSpreadsheetProvider


class AbsSpreadsheetService(ABC):
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

    def read_sheet_data(self, spreadsheet_id, sheet_name):
        if sheet_name not in self.sheet_formats:
            raise KeyError(f"{sheet_name} doesnt' exist in sheet_format config file.")

        data = self.provider.get_sheet_data(spreadsheet_id, sheet_name)
        sheet_format = self.sheet_formats[sheet_name]

        expected_column_names = list(sheet_format.values())

        if list(data.columns) != expected_column_names:
            missing = set(expected_column_names) - set(data.columns)
            extra = set(data.columns) - set(expected_column_names)
            raise SheetSchemaMismatchError(f"Columns mismatch! Missing: {missing}, Extra: {extra}")

        return data


class SpreadsheetService(AbsSpreadsheetService):
    def __init__(self, **kwargs):
        self.sheet_format_path = SHEET_FORMAT_PATH
        super().__init__(**kwargs)


class SpreadsheetServiceByGid(AbsSpreadsheetService):
    def __init__(self, **kwargs):
        self.sheet_format_path = SHEET_FORMAT_BY_GID_PATH
        super().__init__(**kwargs)
