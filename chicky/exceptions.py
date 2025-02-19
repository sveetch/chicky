"""
Specific application exceptions.
"""


class ChickyBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class AppOperationError(ChickyBaseException):
    """
    Sample exception to raise from your code.
    """
    pass
