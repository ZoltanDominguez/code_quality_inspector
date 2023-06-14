from dataclasses import dataclass
from typing import Dict

from code_quality_inspector.reporting.coverage.data_model.coverage_file_model import (
    FileCoverage,
)

FileCoverages = Dict[str, FileCoverage]


@dataclass
class CoverageData:
    coverage: float
    valid: int
    covered: int


@dataclass
class CoverageModel:
    overall_branch_coverage: CoverageData
    overall_line_coverage: CoverageData
    coverages_per_file: FileCoverages
