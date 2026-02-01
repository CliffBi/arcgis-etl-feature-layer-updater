class ArcGisProviderError(Exception):
    """
    Raised when uploading data to an ArcGIS feature layer fails.
    """
    pass


class ArcGisProviderUploadError(Exception):
    """
    Raised when uploading data to an ArcGIS feature layer fails.
    """
    pass


class ArcGisProviderDeleteError(Exception):
    """
    Raised when deleting all data from an ArcGIS feature layer fails.
    """
    pass