from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, Extra, Field

from cqi.app.endpoints import GITHUB_WEBHOOK_ENDPOINT
from cqi.db_connector.dynamodb import DBClient, get_db_connector
from cqi.github_connector.comment_to_pr import comment_to_pr
from cqi.reporting.coverage.coverage_reporting import CoverageReporting
from cqi.reporting.report_interface import ReportingInterface, StoredReporting

github_webhook_router = APIRouter()

# pylint: disable=too-few-public-methods


class Repository(BaseModel):
    name: str
    full_name: str

    class Config:
        extra = Extra.ignore


class Branch(BaseModel):
    ref: str = Field(..., title="Name of the branch (example: 'main, dev')")
    repo: Repository

    class Config:
        extra = Extra.ignore


class PR(BaseModel):
    url: str
    issue_url: str
    pr_id: int = Field(alias="number")
    base: Branch
    head: Branch

    class Config:
        extra = Extra.ignore


class GitHubPRWebhook(BaseModel):
    action: str = Field(..., title="User's user login name")
    repository: Repository
    pull_request: PR

    class Config:
        extra = Extra.ignore


@github_webhook_router.post(
    path=GITHUB_WEBHOOK_ENDPOINT + "/{project_name}",
)
def webhook(
    project_name: str,
    webhook_payload: GitHubPRWebhook,
    db_connector: DBClient = Depends(get_db_connector),
) -> Response:
    pr_id = webhook_payload.pull_request.pr_id
    full_name = webhook_payload.repository.full_name
    base_branch_name = webhook_payload.pull_request.base.ref
    source_branch_name = webhook_payload.pull_request.head.ref

    message = generate_diff_message(
        db_connector=db_connector,
        project_name=project_name,
        source_branch_name=source_branch_name,
        base_branch_name=base_branch_name,
        reporting_class=CoverageReporting(),
    )
    comment_to_pr(repo_full_name=full_name, pr_id=pr_id, content=message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def generate_diff_message(
    db_connector: DBClient,
    project_name: str,
    source_branch_name: str,
    base_branch_name: str,
    reporting_class: ReportingInterface,
) -> str:
    target_report = get_report(
        db_connector=db_connector,
        report_name=reporting_class.report_db_key,
        project_name=project_name,
        branch_name=base_branch_name,
    )
    source_report = get_report(
        db_connector=db_connector,
        report_name=reporting_class.report_db_key,
        project_name=project_name,
        branch_name=source_branch_name,
    )
    message = reporting_class.generate_diff_message(
        target=target_report, source=source_report
    )
    return message


def get_report(
    db_connector: DBClient,
    report_name: str,
    project_name: str,
    branch_name: str,
) -> StoredReporting:
    report = db_connector.get_report(project=project_name, branch=branch_name).get(
        report_name, {}
    )
    return StoredReporting(data=report)
