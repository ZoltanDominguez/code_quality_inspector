from fastapi import APIRouter

from cqi.app.endpoints import GITHUB_WEBHOOK_ENDPOINT
from cqi.github_connector.comment_to_pr import comment_to_pr

github_webhook_router = APIRouter()


@github_webhook_router.post(
    path=GITHUB_WEBHOOK_ENDPOINT,
)
def reports() -> None:
    comment_to_pr(repo_full_name="demo", pr_id=1, content="description")
