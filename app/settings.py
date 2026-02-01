import os

# Path to sheet format files
SHEET_FORMAT_PATH = "sheet_formats/sheet_format.json"
SHEET_FORMAT_BY_GID_PATH = "sheet_formats/sheet_format_by_gid.json"

# Google Spreadsheet
GOOGLE_SPREADSHEET_BY_NAME_URL = "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:json&sheet={1}"
GOOGLE_SPREADSHEET_BY_GID_URL = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv&gid={1}"

# ArcGis
GIS_URL = "https://magneticonegis.maps.arcgis.com"
GIS_USERNAME = os.getenv('GIS_USERNAME')
GIS_PASSWORD = os.getenv('GIS_PASSWORD')
GIS_ITEM_ID = os.getenv('GIS_ITEM_ID')

SPATIAL_REFERENCE_WKID = 4326
