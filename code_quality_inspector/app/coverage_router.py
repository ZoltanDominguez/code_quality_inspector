from fastapi import APIRouter, Depends, File, Form, Path, UploadFile

from code_quality_inspector.app.endpoints import COVERAGE_ENDPOINT
from code_quality_inspector.app.errors import FileNotPresent
from code_quality_inspector.db_connector.dynamodb import (
    DBClient,
    DBSchemaNames,
    get_db_connector,
)
from code_quality_inspector.log import get_logger
from code_quality_inspector.reporting.coverage.coverage_reporting import (
    CoverageReporting,
)
from code_quality_inspector.reporting.report_interface import InputReporting

coverage_router = APIRouter()
logger = get_logger(__name__)

COVERAGE_DESC = """Upload coverage report here."""
COVERAGE_FILE_DESC = "Coverage file in xml format."
HASH_DESC = "Hash uniquely identifying revision"
PROJECT_NAME_DESC = "Name of the project"
TEST_NAME_DESC = "Name of the test ex.: unit, functional, etc."
BRANCH_DESC = "Branch name"


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
):  # pylint: disable=R0913
    try:
        data = file.file.read()
    except AttributeError as exc:
        raise FileNotPresent from exc

    stored_report = CoverageReporting.generate_upload_data(
        reporting_input=InputReporting(branch_name=branch, data=data)
    )
    db_record = db_connector.get_report(project=project_name, branch=branch)
    db_record[DBSchemaNames.coverage] = db_record.get(DBSchemaNames.coverage, {})
    db_record[DBSchemaNames.coverage][test_name] = stored_report
    logger.info(
        "Updated coverage report: %s", db_record[DBSchemaNames.coverage][test_name]
    )
    db_record[DBSchemaNames.commit_hash] = revision_hash
    db_connector.put_report(report=db_record)
    return db_record
