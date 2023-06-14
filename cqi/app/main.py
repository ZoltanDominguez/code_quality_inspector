from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from cqi.app.coverage_router import coverage_router
from cqi.app.errors import CQIBaseException
from cqi.app.middlewares import LoggerMiddleware
from cqi.app.webhook_router import github_webhook_router
from cqi.log import get_logger

logger = get_logger(name="main")

app = FastAPI()
app.include_router(router=coverage_router)
app.include_router(router=github_webhook_router)
app.add_middleware(LoggerMiddleware, logger=logger)


@app.exception_handler(CQIBaseException)
async def api_exception_handler(_: Request, exc: CQIBaseException) -> JSONResponse:
    logger.error("Exception happened. %s is: %s", exc.__class__.__name__, str(exc))
    return JSONResponse(status_code=422, content=exc.api_error)
