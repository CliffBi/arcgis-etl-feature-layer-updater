from typing import List, Optional, Tuple, Dict

from arcgis import GIS
from arcgis.features import FeatureLayer, FeatureSet

from app.settings import GIS_URL, GIS_USERNAME, GIS_PASSWORD, GIS_ITEM_ID


class ArcGisProvider:
    def __init__(self):
        self.connection = self.get_connection()
        self.feature_layer = self.get_feature_layer()

    @staticmethod
    def get_connection() -> GIS:
        connection_params = {'url': GIS_URL}

        if GIS_USERNAME:
            connection_params['username'] = GIS_USERNAME

        if GIS_PASSWORD:
            connection_params['password'] = GIS_PASSWORD

        return GIS(**connection_params)

    def get_feature_layer(self) -> FeatureLayer:
        item = self.connection.content.get(GIS_ITEM_ID)

        if not item:
            raise RuntimeError("Feature Layer item not found")

        return item.layers[0]


    def get_existing_index(self) -> Dict[Tuple[str, str, str], str]:
        index = {}

        object_id_field = self.feature_layer.properties.objectIdField

        features = self.feature_layer.query(
            where="1=1",
            out_fields=f"{object_id_field},date_1,Область,city",
            return_geometry=False
        ).features

        for feature in features:
            key = (
                feature.attributes["date_1"],
                feature.attributes["Область"],
                feature.attributes["city"],
            )
            index[key] = feature.attributes[object_id_field]

        return index

    def upload(self, adds: Optional[List[FeatureSet]], updates: Optional[List[FeatureSet]]) -> None:
        self.feature_layer.edit_features(adds=adds, updates=updates)

    def delete_all_points(self) -> None:
        self.feature_layer.delete_features(where='1=1')