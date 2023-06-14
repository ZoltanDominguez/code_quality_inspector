from fastapi import APIRouter, Response, status

from cqi.app.endpoints import GITHUB_WEBHOOK_ENDPOINT
from cqi.github_connector.comment_to_pr import comment_to_pr

github_webhook_router = APIRouter()


@github_webhook_router.post(
    path=GITHUB_WEBHOOK_ENDPOINT + "/{project_name}",
)
def webhook() -> Response:
    comment_to_pr(repo_full_name="demo", pr_id=1, content="description")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
