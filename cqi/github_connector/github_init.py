import os

from github import Github

from cqi.log import get_logger

logger = get_logger(__name__)


def get_github_connection() -> Github:
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        logger.warning(msg="GITHUB_TOKEN is not found.")
    return Github(login_or_token=github_token)
