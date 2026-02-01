import json
import logging
from abc import ABC, abstractmethod
from urllib.error import HTTPError

import pandas as pd
import requests

from app.spreadsheet.exceptions import SheetProviderError, SheetProviderJsonDecodeError, SheetProviderRequestError
from app.settings import GOOGLE_SPREADSHEET_BY_NAME_URL, GOOGLE_SPREADSHEET_BY_GID_URL

logger = logging.getLogger(__name__)


class AbsSpreadsheetProvider(ABC):
    """
    Abstract base class for interacting with spreadsheets.
    Defines the interface for retrieving spreadsheet data.
    """
    @abstractmethod
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        """
        Retrieve data from a spreadsheet.

        Args:
            spreadsheet_id: The ID of the spreadsheet
            sheet_name: The name or identifier of the sheet

        Returns:
            DataFrame containing the spreadsheet data
        """
        raise NotImplementedError()


class SpreadSheetProvider(AbsSpreadsheetProvider):
    """
    Spreadsheet provider that fetches data using sheet names.
    """
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        """
        Retrieve data from a spreadsheet using the sheet name.
        If the specified sheet name does not exist, returns the first sheet.

        Args:
            spreadsheet_id: The ID of the spreadsheet
            sheet_name: The name of the sheet to fetch

        Returns:
            DataFrame containing the spreadsheet data
        """
        logger.info(f'Getting data from spreadsheet {spreadsheet_id}.')
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

            df =  pd.DataFrame(rows, columns=columns)

            logger.info('Getting data completed.')
            return df

        except requests.RequestException as e:
            logger.error(f'Error: {e}')
            raise SheetProviderRequestError(e)

        except json.JSONDecodeError as e:
            logger.error(f'Error: {e}')
            raise SheetProviderJsonDecodeError(e)

        except Exception as e:
            logger.error(f'Error: {e}')
            raise SheetProviderError(e)


class GidSpreadSheetProvider(AbsSpreadsheetProvider):
    """
    Spreadsheet provider that fetches data using Google sheet GID.
    """
    def get_sheet_data(self, spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
        """
        Retrieve data from a spreadsheet using the sheet GID.
        Raises an error if the specified GID does not exist.

        Args:
            spreadsheet_id: The ID of the spreadsheet
            sheet_name: The GID of the sheet to fetch

        Returns:
            DataFrame containing the spreadsheet data
        """
        try:
            logger.info(f'Getting data from spreadsheet {spreadsheet_id}.')
            df = pd.read_csv(GOOGLE_SPREADSHEET_BY_GID_URL.format(spreadsheet_id, sheet_name))
            logger.info('Getting data completed.')
            return df

        except HTTPError as e:
            logger.error(f'Error: {e}')
            raise SheetProviderRequestError(e)

        except Exception as e:
            logger.error(f'Error: {e}')
            raise SheetProviderError(e)
