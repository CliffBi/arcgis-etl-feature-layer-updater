import logging

from arcgis.features import Feature, FeatureSet

from app.arcgis.provider import ArcGisProvider
from app.columns import data_table_columns
from app.settings import SPATIAL_REFERENCE_WKID
from app.spreadsheet.connector import SpreadsheetConnector, GidSpreadsheetConnector

logger = logging.getLogger(__name__)


class TLayerObserver:
    def __init__(
        self,
        spreadsheet_connector: SpreadsheetConnector,
        gis_provider: ArcGisProvider
    ):
        self.spreadsheet_connector = spreadsheet_connector
        self.gis_provider = gis_provider

    def update_t_layer(self) -> None:
        logger.info('Start updating data to t_layer.')
        add_features = []
        update_features = []

        data_table = self.spreadsheet_connector.data_sheet

        existing_index = self.gis_provider.get_existing_index()

        for _, row in data_table.iterrows():
            long = float(row["long"].replace(',', '.'))
            lat = float(row["lat"].replace(',', '.'))

            base_attributes = {
                "date_1": row["Дата"],
                "Область": row["Область"],
                "city": row["Місто"],
                "long": long,
                "lat": lat
            }

            geometry = {
                "x": long,
                "y": lat,
                "spatialReference": {"wkid": SPATIAL_REFERENCE_WKID},
            }

            row_values = {column: int(row[column]) for column in data_table_columns if int(row[column]) > 0}

            max_count = max(row_values.values(), default=0)

            key = (
                base_attributes["date_1"],
                base_attributes["Область"],
                base_attributes["city"],
            )

            for cnt in range(max_count):
                attributes = base_attributes.copy()

                for col in data_table_columns:
                    idx = col.split()[-1]

                    attributes[f"value_{idx}"] = int(cnt < row_values.get(col, 0))

                if key in existing_index:
                    attributes["OBJECTID"] = existing_index[key]

                    update_features.append(Feature(attributes=attributes, geometry=geometry))
                else:
                    add_features.append(Feature(attributes=attributes, geometry=geometry))

        adds_fs = FeatureSet(features=add_features) if add_features else None
        updates_fs = FeatureSet(features=update_features) if update_features else None

        logger.info(f'Items number to add: {len(adds_fs) if adds_fs else None}')
        logger.info(f'Items number to update: {len(updates_fs) if updates_fs else None}')

        self.gis_provider.upload(adds_fs, updates_fs)
        logger.info('Finish updating data to t_layer.')


class GidTLayerObserver:
    def __init__(
        self,
        spreadsheet_connector: GidSpreadsheetConnector,
        gis_provider: ArcGisProvider
    ):
        self.spreadsheet_connector = spreadsheet_connector
        self.gis_provider = gis_provider

    def update_t_layer(self) -> None:
        logger.info('Start updating data to t_layer.')
        add_features = []
        update_features = []

        zero_table = self.spreadsheet_connector.zero_sheet

        existing_index = self.gis_provider.get_existing_index()

        for _, row in zero_table.iterrows():
            long = float(row["long"].replace(',', '.'))
            lat = float(row["lat"].replace(',', '.'))

            base_attributes = {
                "date_1": row["Дата"],
                "Область": row["Область"],
                "city": row["Місто"],
                "long": long,
                "lat": lat
            }

            geometry = {
                "x": long,
                "y": lat,
                "spatialReference": {"wkid": SPATIAL_REFERENCE_WKID},
            }

            row_values = {column: int(row[column]) for column in data_table_columns if int(row[column]) > 0}

            max_count = max(row_values.values(), default=0)

            key = (
                base_attributes["date_1"],
                base_attributes["Область"],
                base_attributes["city"],
            )

            for cnt in range(max_count):
                attributes = base_attributes.copy()

                for col in data_table_columns:
                    idx = col.split()[-1]

                    attributes[f"value_{idx}"] = (1 if col in row_values and cnt < row_values[col] else 0)

                if key in existing_index:
                    attributes["OBJECTID"] = existing_index[key]

                    update_features.append(Feature(attributes=attributes, geometry=geometry))
                else:
                    add_features.append(Feature(attributes=attributes, geometry=geometry))

        adds_fs = FeatureSet(features=add_features) if add_features else None
        updates_fs = FeatureSet(features=update_features) if update_features else None

        logger.info(f'Items number to add: {len(adds_fs) if adds_fs else None}')
        logger.info(f'Items number to update: {len(updates_fs) if updates_fs else None}')

        self.gis_provider.upload(adds_fs, updates_fs)
        logger.info('Finish updating data to t_layer.')
