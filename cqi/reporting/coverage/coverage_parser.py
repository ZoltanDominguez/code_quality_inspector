from typing import Any, Optional

from cqi.reporting.coverage.data_model.coverage_file_model import (
    FileCoverage,
)
from cqi.reporting.coverage.data_model.coverage_model import (
    FileCoverages,
)

XMLClassObjectT = dict[str, str]


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    return round(float(value) * 100, 4)


def parse_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    return int(value)


def get_file_coverages(coverage_dictionary: dict[str, Any]) -> FileCoverages:
    packages = (
        coverage_dictionary.get("coverage", {}).get("packages", {}).get("package", [])
    )
    file_coverages: FileCoverages = {}
    for package in packages:
        package_classes = package.get("classes", {}).get("class", [])
        if isinstance(package_classes, list):
            for class_object in package_classes:
                append_class_object(
                    class_object=class_object, file_coverages=file_coverages
                )
        if isinstance(package_classes, dict):
            append_class_object(
                class_object=package_classes, file_coverages=file_coverages
            )

    return file_coverages


def append_class_object(
    class_object: XMLClassObjectT, file_coverages: FileCoverages
) -> None:
    try:
        file_coverage = parse_class_object(class_object=class_object)
        file_coverages[file_coverage.filename] = file_coverage
    except ValueError:
        pass


def parse_class_object(class_object: XMLClassObjectT) -> FileCoverage:
    filename = class_object.get("@filename")
    line_rate = parse_float(class_object.get("@line-rate"))
    branch_rate = parse_float(class_object.get("@branch-rate"))

    if not filename:
        raise ValueError("filename is empty")
    if not line_rate:
        raise ValueError("line_rate is empty")
    if not branch_rate:
        raise ValueError("branch_rate is empty")

    return FileCoverage(filename=filename, line_rate=line_rate, branch_rate=branch_rate)
