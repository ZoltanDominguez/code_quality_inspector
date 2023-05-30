import datetime

from github.PullRequest import PullRequest

from code_quality_inspector.github_connector.github_init import GITHUB

GITHUB_USER_NAME = GITHUB.get_user().name


def get_pull_request(pr_id: int, repo_full_name: str) -> PullRequest:
    repo = GITHUB.get_repo(repo_full_name)
    pr = repo.get_pull(pr_id)
    return pr


def append_timestamp(content: str) -> str:
    return f"{datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}\n\n{content}"


def create_new_comment(pr: PullRequest, content: str):
    pr.create_issue_comment(content)
