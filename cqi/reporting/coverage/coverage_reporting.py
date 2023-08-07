from typing import Any, Optional, Tuple

import xmltodict
from pydantic import ValidationError

from cqi.app.errors import MalformedDataEntry
from cqi.log import get_logger
from cqi.reporting.coverage.coverage_parser import (
    get_file_coverages,
    parse_float,
    parse_int,
)
from cqi.reporting.coverage.data_model import CoverageData, CoverageModel
from cqi.reporting.coverage.data_model.coverage_model import FileCoverage, FileCoverages
from cqi.reporting.coverage.message_utils import (
    get_coverage_compare_message,
    get_message_for_max_coverage_diffs,
)
from cqi.reporting.report_interface import (
    InputReporting,
    ReportingInterface,
    StoredReporting,
)

logger = get_logger(__name__)
FILE_DIFFERENCES_COUNT_MAX = 5


class CoverageReporting(ReportingInterface):
    report_name = "Coverage report"
    report_db_key = "coverage"

    @staticmethod
    def generate_upload_data(reporting_input: InputReporting) -> StoredReporting:
        """Parsing from raw coverage file to CoverageModel"""
        xml = xmltodict.parse(reporting_input.data)

        branch_coverage = xml.get("coverage", {}).get("@branch-rate", None)
        line_coverage = xml.get("coverage", {}).get("@line-rate", None)
        lines_valid = xml.get("coverage", {}).get("@lines-valid", None)
        lines_covered = xml.get("coverage", {}).get("@lines-covered", None)
        branches_valid = xml.get("coverage", {}).get("@branches-valid", None)
        branches_covered = xml.get("coverage", {}).get("@branches-covered", None)

        branch_coverage = parse_float(value=branch_coverage)
        line_coverage = parse_float(value=line_coverage)
        lines_valid = parse_int(value=lines_valid)
        lines_covered = parse_int(value=lines_covered)
        branches_valid = parse_int(value=branches_valid)
        branches_covered = parse_int(value=branches_covered)

        file_coverages = get_file_coverages(coverage_dictionary=xml)

        coverage_data = CoverageModel(
            overall_branch_coverage=CoverageData(
                coverage=branch_coverage, valid=branches_valid, covered=branches_covered
            ),
            overall_line_coverage=CoverageData(
                coverage=line_coverage, valid=lines_valid, covered=lines_covered
            ),
            coverages_per_file=file_coverages,
        )
        return StoredReporting(
            data={
                reporting_input.type: coverage_data.dict(),
            },
        )

    @staticmethod
    def generate_diff_message(target: StoredReporting, source: StoredReporting) -> str:
        """
        Parsing from 2 serialized StoredReporting.
        Create diff message from the 2 CoverageModels per coverage type.
        """
        common_test_types = get_common_test_types(target=target, source=source)
        message = []
        for common_test_name in common_test_types:
            source_cov, target_cov = parse_coverages(
                source=source.data.get(common_test_name),
                target=target.data.get(common_test_name),
            )
            report = get_coverage_compare_message(target=target_cov, source=source_cov)
            if report:
                message.append(
                    f"{common_test_name} test coverage change:\n".capitalize()
                )
                message.append(report)

        for common_test_name in common_test_types:
            message.append("\n")
            source_cov, target_cov = parse_coverages(
                source=source.data.get(common_test_name),
                target=target.data.get(common_test_name),
            )
            report = get_max_coverage_diffs_message(
                target=target_cov, source=source_cov
            )
            if report:
                message.append(
                    f"Largest {common_test_name} test coverage changes per file:\n"
                )
                message.append(report)
        return "".join(message)


def parse_coverages(
    source: Optional[Any], target: Optional[Any]
) -> Tuple[CoverageModel, CoverageModel]:
    """
    Parses from the stored report source and target to CoverageModel instances.

    Raises:
        MalformedDataEntry: When pydantic cannot parse to the CoverageModel
    """
    try:
        target_cov = CoverageModel.parse_obj(target)
    except ValidationError as exc:
        logger.error(f"Error parsing target coverage. {exc}")
        raise MalformedDataEntry from exc
    try:
        source_cov = CoverageModel.parse_obj(source)
    except ValidationError as exc:
        logger.error(f"Error parsing source coverage. {exc}")
        raise MalformedDataEntry from exc
    return source_cov, target_cov


def get_common_test_types(target: StoredReporting, source: StoredReporting) -> set[str]:
    source_coverage_types = set(source.data.keys())
    target_coverage_types = set(target.data.keys())
    common_coverage_types = source_coverage_types.intersection(target_coverage_types)
    logger.info(
        f"Common coverage types: {common_coverage_types}. "
        f"Source test types: {source_coverage_types}, "
        f"Target test types: {target_coverage_types}"
    )
    return common_coverage_types


def get_max_coverage_diffs_message(
    target: CoverageModel,
    source: CoverageModel,
) -> str:
    max_coverage_diffs = get_max_coverage_diffs(
        source_coverages=source.coverages_per_file,
        target_coverages=target.coverages_per_file,
        count=FILE_DIFFERENCES_COUNT_MAX,
    )

    message = get_message_for_max_coverage_diffs(
        max_coverage_diffs,
        target_coverages=target.coverages_per_file,
        source_coverages=source.coverages_per_file,
    )
    return message


def get_max_coverage_diffs(
    source_coverages: FileCoverages,
    target_coverages: FileCoverages,
    count: int,
) -> list[FileCoverage]:
    """Returns a list of FileCoverages sorted by line_rate"""
    coverage_diffs = {}
    for filename, target_coverage in target_coverages.items():
        if filename not in source_coverages:
            continue
        coverage_diffs[filename] = source_coverages[filename] - target_coverage

    coverage_diffs_list = list(coverage_diffs.values())
    coverage_diffs_list.sort(key=lambda v: abs(v.line_rate), reverse=True)
    max_coverage_diffs = coverage_diffs_list[:count]

    return max_coverage_diffs
