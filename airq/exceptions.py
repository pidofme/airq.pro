class AirqError(Exception):
    """Exception raised for errors in airq.

    Attributes:
        status_code -- http status code
        message -- explanation of the error
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
