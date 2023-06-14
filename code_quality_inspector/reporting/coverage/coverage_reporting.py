from dataclasses import asdict

import xmltodict

from code_quality_inspector.reporting.coverage.coverage_parser import (
    get_file_coverages,
    parse_float,
    parse_int,
)
from code_quality_inspector.reporting.coverage.data_model import (
    CoverageData,
    CoverageModel,
)
from code_quality_inspector.reporting.report_interface import (
    InputReporting,
    ReportingInterface,
    StoredReporting,
)


class CoverageReporting(ReportingInterface):
    report_name = "Coverage report"

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
            branch_name=reporting_input.branch_name, data=asdict(coverage_data)
        )

    @staticmethod
    def generate_diff_message(target: StoredReporting, source: StoredReporting) -> str:
        """
        Parsing from 2 serialized CoverageModels in StoredReporting.
        Create diff message from the 2 CoverageModels.
        """
        raise NotImplementedError
