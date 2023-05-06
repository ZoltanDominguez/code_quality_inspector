import datetime
import os
from typing import List

from github import Github
from github.IssueComment import IssueComment
from github.PullRequest import PullRequest

from code_quality_inspector.log import get_logger

logger = get_logger(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    logger.warning(msg="GITHUB_TOKEN is not found.")

GITHUB = Github(login_or_token=GITHUB_TOKEN)


def comment_to_pr(repo_full_name: str, pr_id: int, content: str):
    pr = get_pull_request(pr_id=pr_id, repo_full_name=repo_full_name)
    if pr.state != "open":
        logger.error(msg="Not commenting to PR that is not open.")
        return

    content = append_timestamp(content)
    create_new_comment(pr, content=content)
    delete_older_comments_by_current_user(pr)


def get_pull_request(pr_id: int, repo_full_name: str) -> PullRequest:
    repo = GITHUB.get_repo(repo_full_name)
    pr = repo.get_pull(pr_id)
    return pr


def append_timestamp(content: str) -> str:
    return f"{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}\n\n{content}"


def delete_older_comments_by_current_user(pr: PullRequest):
    comments = pr.get_issue_comments()
    comments_created_by_this_user = get_comments_created_by_this_user(comments)
    for comment in get_comments_to_delete(comments_created_by_this_user):
        comment.delete()


def get_comments_created_by_this_user(
    comments: List[IssueComment],
) -> List[IssueComment]:
    comments_created_by_this_user = []
    for comment in comments:
        if comment.user.name == GITHUB.get_user().name:
            logger.info(
                msg=f"Found previous comment: "
                f"{comment.created_at}, {comment.user.login}, {comment.body}"
            )
            comments_created_by_this_user.append(comment)
    return comments_created_by_this_user


def get_comments_to_delete(comments: List[IssueComment]) -> List[IssueComment]:
    comments.sort(key=lambda comment: comment.created_at)
    return comments[:-1]


def create_new_comment(pr: PullRequest, content: str):
    pr.create_issue_comment(content)
