from fastapi import FastAPI

from code_quality_inspector.app.coverage_router import coverage_router
from code_quality_inspector.app.webhook_router import github_webhook_router

app = FastAPI()
app.include_router(router=coverage_router)
app.include_router(router=github_webhook_router)
