from cqi.log import get_logger
from cqi.reporting.coverage.data_model import CoverageModel
from cqi.reporting.coverage.data_model.coverage_model import FileCoverage, FileCoverages

ROUND_DIGITS = 2

FAILURE_EMOJI = ":red_circle:"
SUCCESS_EMOJI = ":green_circle:"

logger = get_logger(__name__)


def plus_sign_generator(difference: float) -> str:
    return "+" if difference >= 0 else ""


def emoji_generator(difference: float) -> str:
    return SUCCESS_EMOJI if difference >= 0 else FAILURE_EMOJI


def get_message_for_max_coverage_diffs(
    max_coverage_diffs: list[FileCoverage],
    target_coverages: FileCoverages,
    source_coverages: FileCoverages,
) -> str:
    """Returns a message for max file coverage differences sorted by line_rate"""
    if not max_coverage_diffs or max_coverage_diffs[0].line_rate == 0:
        return "No significant line coverage difference was found."

    message = "| File name | Line cov. change | Difference |\n|---|---|---|\n"
    for file_coverage in max_coverage_diffs:
        target_coverage = target_coverages[file_coverage.filename]
        branch_coverage = source_coverages[file_coverage.filename]

        branch_cov_diff = round(
            (branch_coverage.line_rate - target_coverage.line_rate) * 100, 2
        )
        branch_cov_diff_emoji = emoji_generator(branch_cov_diff)
        branch_cov_diff_sign = plus_sign_generator(branch_cov_diff)

        message += (
            f"| {file_coverage.filename} | "
            f"{round(target_coverage.line_rate*100, 2)}% -> "
            f"{round(branch_coverage.line_rate*100, 2)}%  |  "
            f"{branch_cov_diff_sign}{branch_cov_diff}% {branch_cov_diff_emoji} |\n"
        )

    return message


def get_coverage_compare_message(
    target: CoverageModel,
    source: CoverageModel,
) -> str:
    target_branch_cov = round(
        target.overall_branch_coverage.coverage * 100, ROUND_DIGITS
    )
    source_branch_cov = round(
        source.overall_branch_coverage.coverage * 100, ROUND_DIGITS
    )
    target_line_cov = round(target.overall_line_coverage.coverage * 100, ROUND_DIGITS)
    source_line_cov = round(source.overall_line_coverage.coverage * 100, ROUND_DIGITS)

    branch_cov_diff = round(source_branch_cov - target_branch_cov, ROUND_DIGITS)
    branch_cov_diff_emoji = emoji_generator(branch_cov_diff)
    branch_cov_diff_sign = plus_sign_generator(branch_cov_diff)

    line_cov_diff = round(source_line_cov - target_line_cov, ROUND_DIGITS)
    line_cov_diff_emoji = emoji_generator(line_cov_diff)
    line_cov_diff_sign = plus_sign_generator(line_cov_diff)

    return (
        "| Metric | Change | Difference |\n"
        "|---|---|---|\n"
        f"| Branch coverage | "
        f"{target_branch_cov}% -> {source_branch_cov}%  |  "
        f"{branch_cov_diff_sign}{branch_cov_diff}% {branch_cov_diff_emoji} |\n"
        f"| Line coverage   | "
        f"{target_line_cov}% -> {source_line_cov}%  |  "
        f"{line_cov_diff_sign}{line_cov_diff}% {line_cov_diff_emoji} |\n"
    )
