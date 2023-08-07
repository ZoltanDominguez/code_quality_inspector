from typing import List

from github.IssueComment import IssueComment
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest

from cqi.github_connector.github_utils import (
    append_timestamp,
    create_new_comment,
    get_pull_request,
    get_user_name,
)
from cqi.log import get_logger

logger = get_logger(__name__)


def comment_to_pr(repo_full_name: str, pr_id: int, content: str) -> None:
    pr = get_pull_request(pr_id=pr_id, repo_full_name=repo_full_name)
    if pr.state != "open":
        logger.error("Not commenting to PR that is not open.")
        return

    content = append_timestamp(content)
    logger.info("Creating GitHub Comment: %s", content)
    create_new_comment(pr, content=content)
    delete_older_comments_by_current_user(pr=pr)


def delete_older_comments_by_current_user(pr: PullRequest) -> None:
    comments = pr.get_issue_comments()
    comments_created_by_this_user = get_comments_created_by_this_user(comments=comments)
    for comment in get_comments_to_delete(comments=comments_created_by_this_user):
        comment.delete()


def get_comments_created_by_this_user(
    comments: PaginatedList,  # type: ignore
) -> List[IssueComment]:
    comments_created_by_this_user = []
    for comment in comments:
        if comment.user.name == get_user_name():
            logger.info(
                msg=f"Found previous comment: "
                f"{comment.created_at}, {comment.user.login}, {comment.body}"
            )
            comments_created_by_this_user.append(comment)
    return comments_created_by_this_user


def get_comments_to_delete(comments: List[IssueComment]) -> List[IssueComment]:
    comments.sort(key=lambda comment: comment.created_at)
    return comments[:-1]
