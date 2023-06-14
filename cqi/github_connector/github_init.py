import os

from github import Github

from cqi.log import get_logger

logger = get_logger(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    logger.warning(msg="GITHUB_TOKEN is not found.")
GITHUB = Github(login_or_token=GITHUB_TOKEN)
