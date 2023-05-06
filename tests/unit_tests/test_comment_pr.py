from datetime import datetime
from unittest.mock import Mock

from code_quality_inspector.github_connector.comment_to_pr import get_comments_to_delete


def test_comment_deletion_based_on_datetime():
    date_1 = datetime(2010, 1, 1, 18, 00)
    date_2 = datetime(2010, 1, 1, 19, 00)
    date_3 = datetime(2010, 1, 1, 18, 30)
    comments = [
        Mock(created_at=date_1),
        Mock(created_at=date_2),
        Mock(created_at=date_3),
    ]

    comments_to_delete = get_comments_to_delete(comments)
    for comment in comments_to_delete:
        print(comment.created_at)
        assert comment.created_at != date_2
    assert len(comments_to_delete) == 2
