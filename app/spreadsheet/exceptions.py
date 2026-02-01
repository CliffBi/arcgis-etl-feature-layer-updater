class SheetSchemaMismatchError(Exception):
    """
    Raised when data from a Google Spreadsheet does not match the expected schema defined in the sheet_format
    configuration.
    """
    pass


class SheetProviderError(Exception):
    """
    General exception for errors related to the SheetProvider.
    """
    pass


class SheetProviderRequestError(Exception):
    """
    Raised when a request within the SheetProvider fails (e.g., network or HTTP error).
    """
    pass


class SheetProviderJsonDecodeError(Exception):
    """
    Raised when JSON decoding fails within the SheetProvider.
    """
    pass
