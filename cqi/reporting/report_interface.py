from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

InputData = Union[str, bytes]


@dataclass
class InputReporting:
    branch_name: str
    data: InputData
    type: Optional[str] = None


@dataclass
class StoredReporting:
    """Structure stored in the database"""

    data: Dict[Any, Any]


class ReportingInterface(ABC):
    @property
    @abstractmethod
    def report_name(self) -> str:
        """Name of the report that will be displayed"""

    @property
    @abstractmethod
    def report_db_key(self) -> str:
        """Name of the Database key where the report will be stored"""

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
