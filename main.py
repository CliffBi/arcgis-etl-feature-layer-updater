import logging.config
import os

from app import settings
from app.arcgis.provider import ArcGisProvider
from app.observers import TLayerObserver, GidTLayerObserver
from app.spreadsheet.connector import GidSpreadsheetConnector, SpreadsheetConnector
from app.spreadsheet.provider import SpreadSheetProvider, GidSpreadSheetProvider
from app.spreadsheet.services import GidSpreadsheetService, SpreadsheetService

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

spreadsheet_id = os.getenv('OUTPUT_DATA_SPREADSHEET_ID')


def run_upload_data():
    provider = SpreadSheetProvider()
    service = SpreadsheetService(provider=provider)
    connector = SpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=service)
    TLayerObserver(connector, ArcGisProvider()).update_t_layer()


def run_upload_data_by_gid():
    provider = GidSpreadSheetProvider()
    service = GidSpreadsheetService(provider=provider)
    connector = GidSpreadsheetConnector(spreadsheet_id=spreadsheet_id, spreadsheet_service=service)
    GidTLayerObserver(connector, ArcGisProvider()).update_t_layer()


