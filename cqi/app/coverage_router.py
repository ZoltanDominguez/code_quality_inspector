from dataclasses import asdict

from fastapi import APIRouter, Depends, File, Form, Path, Response, UploadFile, status

from cqi.app.endpoints import COVERAGE_ENDPOINT
from cqi.app.errors import FileIsEmpty, FileNotPresent, ItemNotFoundInDatabase
from cqi.db_connector.dynamodb import (
    DBClient,
    DBSchemaNames,
    get_db_connector,
)
from cqi.log import get_logger
from cqi.reporting.coverage.coverage_reporting import (
    CoverageReporting,
)
from cqi.reporting.report_interface import InputReporting

coverage_router = APIRouter()
logger = get_logger(__name__)

COVERAGE_DESC = """Upload coverage report here."""
COVERAGE_FILE_DESC = "Coverage file in xml format uploaded as multipart/form-data."
HASH_DESC = "Hash uniquely identifying revision"
PROJECT_NAME_DESC = "Name of the project"
TEST_NAME_DESC = "Name of the test suite ex.: unit, functional, etc."
BRANCH_DESC = "Branch name the report was generated from"


# pylint: disable=R0913
@coverage_router.post(
    path=COVERAGE_ENDPOINT + "/{project_name}/{test_name}",
    description=COVERAGE_DESC,
)
def coverage_reports(
    project_name: str = Path(description=PROJECT_NAME_DESC, min_length=3),
    test_name: str = Path(description=TEST_NAME_DESC, min_length=3),
    file: UploadFile = File(description=COVERAGE_FILE_DESC),
    revision_hash: str = Form(description=HASH_DESC, min_length=3),
    branch: str = Form(description=BRANCH_DESC, min_length=3),
    db_connector: DBClient = Depends(get_db_connector),
) -> Response:
    logger.info("Adding coverage for: %s-%s", project_name, branch)
    try:
        data = file.file.read()
    except AttributeError as exc:
        raise FileNotPresent from exc

    if not data:
        raise FileIsEmpty

    stored_report = CoverageReporting.generate_upload_data(
        reporting_input=InputReporting(branch_name=branch, data=data)
    )
    try:
        db_record = db_connector.get_report(project=project_name, branch=branch)
        logger.info("Existing report found, updating it with coverage.")
    except ItemNotFoundInDatabase:
        logger.info("No existing report found, creating new.")
        db_record = {}

    report_name = DBSchemaNames.coverage
    db_record[report_name] = db_record.get(report_name, {})
    db_record[report_name][test_name] = asdict(stored_report)
    db_record[DBSchemaNames.revision_hash] = revision_hash

    db_connector.put_report(report=db_record)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
