from fastapi import APIRouter

from code_quality_inspector.app.endpoints import COVERAGE_ENDPOINT

coverage_router = APIRouter()


@coverage_router.post(
    path=COVERAGE_ENDPOINT,
)
def reports():
    return {"Hello": "World"}
