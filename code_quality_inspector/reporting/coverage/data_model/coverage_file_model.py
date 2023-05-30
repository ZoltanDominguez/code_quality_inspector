from dataclasses import dataclass


@dataclass
class FileCoverage:
    filename: str
    line_rate: float
    branch_rate: float

    @classmethod
    def from_string(cls, serial: str):
        filename, line_rate, branch_rate = serial.split(", ")
        return cls(filename, float(line_rate), float(branch_rate))

    def serialize(self):
        return f"{self.filename}, {self.line_rate}, {self.branch_rate}"

    def __sub__(self, other):
        self.check_same_filename(other_file_coverage=other)
        return FileCoverage(
            self.filename,
            self.line_rate - other.line_rate,
            self.branch_rate - other.branch_rate,
        )

    def check_same_filename(self, other_file_coverage):
        if other_file_coverage.filename != self.filename:
            raise ValueError(
                "Subtracting coverage for different files is not supported"
            )
