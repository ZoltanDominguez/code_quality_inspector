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

    @staticmethod
    def generate_diff_message(target: StoredReporting, source: StoredReporting) -> str:
        """
        Parsing from 2 serialized CoverageModels in StoredReporting.
        Create diff message from the 2 CoverageModels.
        """
