from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Union

InputData = Union[str, bytes]


@dataclass
class InputReporting:
    branch_name: str
    data: InputData


@dataclass
class StoredReporting:
    branch_name: str
    data: Union[str, bytes, Dict[Any, Any]]


class ReportingInterface(ABC):
    @property
    @abstractmethod
    def report_name(self) -> str:
        """Name of the report that will be displayed"""

    @staticmethod
    @abstractmethod
    def generate_upload_data(reporting_input: InputReporting) -> StoredReporting:
        """
        Gets one version of the report, gives back a representation that will be stored.
        """

    @staticmethod
    @abstractmethod
    def generate_diff_message(target: StoredReporting, source: StoredReporting) -> str:
        """
        Generates a difference message from the 2 StoredReporting
        """
