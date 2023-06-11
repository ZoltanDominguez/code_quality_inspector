from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from code_quality_inspector.app.coverage_router import coverage_router
from code_quality_inspector.app.errors import CQIBaseException
from code_quality_inspector.app.middlewares import LoggerMiddleware
from code_quality_inspector.app.webhook_router import github_webhook_router
from code_quality_inspector.log import get_logger

logger = get_logger(name="main")

app = FastAPI()
app.include_router(router=coverage_router)
app.include_router(router=github_webhook_router)
app.add_middleware(LoggerMiddleware, logger=logger)


@app.exception_handler(CQIBaseException)
async def api_exception_handler(_: Request, exc: CQIBaseException):
    logger.error("Exception happened. %s is: %s", exc.__class__.__name__, str(exc))
    return JSONResponse(status_code=422, content=exc.api_error)
