import datetime

from github.PullRequest import PullRequest

from cqi.github_connector.github_init import get_github_connection


def get_user_name() -> str:
    return get_github_connection().get_user().name


def get_pull_request(pr_id: int, repo_full_name: str) -> PullRequest:
    repo = get_github_connection().get_repo(repo_full_name)
    pr = repo.get_pull(pr_id)
    return pr


def append_timestamp(content: str) -> str:
    return f"{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}\n\n{content}"


def create_new_comment(pr: PullRequest, content: str) -> None:
    pr.create_issue_comment(content)
