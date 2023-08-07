from __future__ import annotations

from typing import Dict

from pydantic import BaseModel


class FileCoverage(BaseModel):
    filename: str
    line_rate: float
    branch_rate: float

    def __sub__(self, other: FileCoverage) -> FileCoverage:
        self.check_same_filename(other_file_coverage=other)
        return FileCoverage.parse_obj(
            {
                "filename": self.filename,
                "line_rate": self.line_rate - other.line_rate,
                "branch_rate": self.branch_rate - other.branch_rate,
            }
        )

    def check_same_filename(self, other_file_coverage: FileCoverage) -> None:
        if other_file_coverage.filename != self.filename:
            raise ValueError(
                "Subtracting coverage for different files is not supported"
            )


FileCoverages = Dict[str, FileCoverage]


class CoverageData(BaseModel):
    coverage: float
    valid: int
    covered: int


class CoverageModel(BaseModel):
    overall_branch_coverage: CoverageData
    overall_line_coverage: CoverageData
    coverages_per_file: FileCoverages
