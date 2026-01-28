import os

from app.spreadsheet.connector import GidSpreadsheetConnector, SpreadsheetConnector
from app.spreadsheet.provider import SpreadSheetProvider, SpreadSheetByGidProvider
from app.spreadsheet.services import SpreadsheetServiceByGid, SpreadsheetService

if __name__ == '__main__':
    spreadsheet_id = os.getenv('OUTPUT_DATA_SPREADSHEET_ID')

    # Gid
    gid_provider = SpreadSheetByGidProvider()
    gid_service = SpreadsheetServiceByGid(provider=gid_provider)
    gid_connector = GidSpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=gid_service)
    a = gid_connector.zero_sheet

    # Name
    provider = SpreadSheetProvider()
    service = SpreadsheetService(provider=provider)
    connector = SpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=service)
    c = connector.data_sheet
