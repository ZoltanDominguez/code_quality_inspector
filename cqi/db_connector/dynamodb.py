from dataclasses import dataclass
from typing import Any

import boto3
from botocore import exceptions

from cqi.app.errors import (
    GenericDatabaseError,
    ItemNotFoundInDatabase,
)
from cqi.config.config import config
from cqi.log import get_logger

logger = get_logger(__name__)


def parse_dict_to_dynamo_item(dictionary: dict[Any, Any]) -> dict[Any, Any]:
    if isinstance(dictionary, dict):
        _return: dict[Any, Any] = {}
        for key, value in dictionary.items():
            if isinstance(value, float):
                _return[key] = str(value)
            elif isinstance(value, dict):
                _return[key] = parse_dict_to_dynamo_item(value)
            else:
                _return[key] = value
        return _return
    return dictionary


@dataclass
class DBSchemaNames:
    project: str = "project_name"
    branch: str = "branch_name"
    revision_hash: str = "revision_hash"
    coverage: str = "coverage"


class DBClient:
    """DynamoDB client for putting and getting data from the AWS DB instance"""

    def __init__(self) -> None:
        logger.info("DynamoDB table name: %s", config.db.table_name)
        self.table = boto3.resource("dynamodb").Table(config.db.table_name)

    def put_report(self, report: dict[Any, Any]) -> None:
        """Creates or updates a report"""
        item = parse_dict_to_dynamo_item(dictionary=report)
        self.table.put_item(Item=item)

    def get_report(self, project: str, branch: str) -> Any:
        try:
            response = self.table.get_item(
                Key={DBSchemaNames.project: project, DBSchemaNames.branch: branch}
            )
            return response["Item"]
        except exceptions.ClientError as exc:
            logger.error(
                f"Failed to get {project}/{branch} data from Dynamo due to {exc}"
            )
            raise GenericDatabaseError from exc
        except KeyError as exc:
            logger.warning(
                f"Entry with keys: {project=}, {branch=} not found in DynamoDB",
            )
            raise ItemNotFoundInDatabase from exc


def get_db_connector() -> DBClient:
    return DBClient()
