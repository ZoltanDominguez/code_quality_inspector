from typing import TypedDict


class Error(TypedDict):
    error_code: int
    error_message: str


class CQIBaseException(Exception):
    api_error: Error


# -------------------- Generic errors
class GenericError(CQIBaseException):
    api_error = Error(error_code=1000, error_message="Unexpected exception")


# -------------------- Database errors
class GenericDatabaseError(CQIBaseException):
    api_error = Error(error_code=2000, error_message="Generic database error")


class ItemNotFoundInDatabase(GenericDatabaseError):
    api_error = Error(error_code=2001, error_message="Item not found in database")


# -------------------- Validity errors
class FileNotPresent(CQIBaseException):
    api_error = Error(error_code=3001, error_message="File not present")
