import json
from abc import ABC, abstractmethod
from urllib.error import HTTPError

import pandas as pd
import requests

from app.exceptions import SheetProviderError, SheetProviderJsonDecodeError, SheetProviderRequestError
from app.settings import GOOGLE_SPREADSHEET_BY_NAME_URL, GOOGLE_SPREADSHEET_BY_GID_URL


class AbsSpreadsheetProvider(ABC):
    @abstractmethod
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        raise NotImplementedError()


class SpreadSheetProvider(AbsSpreadsheetProvider):
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        try:
            url = GOOGLE_SPREADSHEET_BY_NAME_URL.format(spreadsheet_id, sheet_name)

            response = requests.get(url)
            response.raise_for_status()

            raw_response_data = response.text

            json_data = raw_response_data[raw_response_data.find("{"): raw_response_data.rfind("}") + 1]
            response_data = json.loads(json_data)
            data_table = response_data["table"]

            columns = [c["label"] for c in data_table["cols"]]
            rows = []

            for row in data_table["rows"]:
                rows.append([cell.get("f", cell.get('v')) if cell else None for cell in row["c"]])

            return pd.DataFrame(rows, columns=columns)

        except requests.RequestException as e:
            raise SheetProviderRequestError(e)

        except json.JSONDecodeError as e:
            raise SheetProviderJsonDecodeError(e)

        except Exception as e:
            raise SheetProviderError(e)


class GidSpreadSheetProvider(AbsSpreadsheetProvider):
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        try:
            return pd.read_csv(GOOGLE_SPREADSHEET_BY_GID_URL.format(spreadsheet_id, sheet_name))

        except HTTPError as e:
            raise SheetProviderRequestError(e)

        except Exception as e:
            raise SheetProviderError(e)
