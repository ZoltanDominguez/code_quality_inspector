import pytest

from cqi.app.errors import MalformedDataEntry
from cqi.reporting.coverage.coverage_reporting import CoverageReporting
from cqi.reporting.coverage.data_model import CoverageData, CoverageModel
from cqi.reporting.coverage.data_model.coverage_model import FileCoverage
from cqi.reporting.report_interface import StoredReporting


def test_generate_diff_message():
    target = CoverageModel(
        overall_branch_coverage=CoverageData(coverage=0.812345, valid=100, covered=80),
        overall_line_coverage=CoverageData(coverage=0.712345, valid=100, covered=70),
        coverages_per_file={},
    )
    source = CoverageModel(
        overall_branch_coverage=CoverageData(coverage=0.812345, valid=100, covered=80),
        overall_line_coverage=CoverageData(coverage=0.912345, valid=100, covered=70),
        coverages_per_file={},
    )
    target = StoredReporting(data={"unittest": target.dict()})
    source = StoredReporting(data={"unittest": source.dict()})
    message = CoverageReporting.generate_diff_message(target=target, source=source)
    expected = (
        "Unittest test coverage change:\n"
        "| Metric | Change | Difference |\n"
        "|---|---|---|\n"
        "| Branch coverage | 81.23% -> 81.23%  |  +0.0% :green_circle: |\n"
        "| Line coverage   | 71.23% -> 91.23%  |  +20.0% :green_circle: |\n"
        "\nLargest unittest test coverage changes per file:\n"
        "No significant line coverage difference was found."
    )
    assert message == expected


def test_generate_message_empty():
    target = {}
    source = {}
    target = StoredReporting(data={"unittest": target})
    source = StoredReporting(data={"unittest": source})
    with pytest.raises(MalformedDataEntry):
        _ = CoverageReporting.generate_diff_message(target=target, source=source)


def test_generate_message_no_common():
    target = {}
    source = {}
    target = StoredReporting(data={"unittest": target})
    source = StoredReporting(data={"apitest": source})
    message = CoverageReporting.generate_diff_message(target=target, source=source)
    assert message == ""


def test_generate_diff_message_per_files():
    target = CoverageModel(
        overall_branch_coverage=CoverageData(coverage=0.812345, valid=100, covered=80),
        overall_line_coverage=CoverageData(coverage=0.712345, valid=100, covered=70),
        coverages_per_file={
            "filename1": FileCoverage.parse_obj(
                {"filename": "filename1", "line_rate": 0.5, "branch_rate": 0.6}
            ),
            "filename2": FileCoverage.parse_obj(
                {"filename": "filename2", "line_rate": 0.5, "branch_rate": 0.6}
            ),
        },
    )
    source = CoverageModel(
        overall_branch_coverage=CoverageData(coverage=0.812345, valid=100, covered=80),
        overall_line_coverage=CoverageData(coverage=0.912345, valid=100, covered=70),
        coverages_per_file={
            "filename1": FileCoverage.parse_obj(
                {"filename": "filename1", "line_rate": 0.4, "branch_rate": 0.6}
            ),
            "filename2": FileCoverage.parse_obj(
                {"filename": "filename2", "line_rate": 0.6, "branch_rate": 0.6}
            ),
        },
    )
    target = StoredReporting(data={"unittest": target.dict()})
    source = StoredReporting(data={"unittest": source.dict()})
    message = CoverageReporting.generate_diff_message(target=target, source=source)
    expected = (
        "Unittest test coverage change:\n"
        "| Metric | Change | Difference |\n"
        "|---|---|---|\n"
        "| Branch coverage | 81.23% -> 81.23%  |  +0.0% :green_circle: |\n"
        "| Line coverage   | 71.23% -> 91.23%  |  +20.0% :green_circle: |\n"
        "\nLargest unittest test coverage changes per file:\n"
        "| File name | Line cov. change | Difference |\n"
        "|---|---|---|\n"
        "| filename1 | 50.0% -> 40.0%  |  -10.0% :red_circle: |\n"
        "| filename2 | 50.0% -> 60.0%  |  +10.0% :green_circle: |\n"
    )
    print(message)
    assert message == expected
