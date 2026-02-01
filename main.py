import os

from app.arcgis.provider import ArcGisProvider
from app.observers import TLayerObserver, GidTLayerObserver
from app.spreadsheet.connector import GidSpreadsheetConnector, SpreadsheetConnector
from app.spreadsheet.provider import SpreadSheetProvider, GidSpreadSheetProvider
from app.spreadsheet.services import GidSpreadsheetService, SpreadsheetService

if __name__ == '__main__':
    spreadsheet_id = os.getenv('OUTPUT_DATA_SPREADSHEET_ID')

    # Name
    provider = SpreadSheetProvider()
    service = SpreadsheetService(provider=provider)
    connector = SpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=service)
    TLayerObserver(connector, ArcGisProvider()).update_t_layer()

    # Gid
    gid_provider = GidSpreadSheetProvider()
    gid_service = GidSpreadsheetService(provider=gid_provider)
    gid_connector = GidSpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=gid_service)
    GidTLayerObserver(gid_connector, ArcGisProvider()).update_t_layer()
