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


class ItemNotDictionaryInDatabase(GenericDatabaseError):
    api_error = Error(
        error_code=2002, error_message="Item is not in dictionary format in database"
    )


# -------------------- Endpoint Validity errors
class FileNotPresent(CQIBaseException):
    api_error = Error(error_code=3001, error_message="File not present")


class FileIsEmpty(CQIBaseException):
    api_error = Error(error_code=3002, error_message="File is empty")


# -------------------- Reporting Validity errors
class MalformedDataEntry(CQIBaseException):
    api_error = Error(error_code=4001, error_message="Data entry is malformed")
