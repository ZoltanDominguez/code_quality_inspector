from logging import INFO, Logger

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LoggerMiddleware:  # pylint: disable=too-few-public-methods
    app: ASGIApp

    def __init__(
        self,
        app: ASGIApp,
        logger: Logger,
    ) -> None:
        self.app = app
        self.logger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def handle_outgoing_request(message: Message) -> None:
            if (
                self.logger.isEnabledFor(INFO)
                and message["type"] == "http.response.start"
            ):
                response_headers = MutableHeaders(scope=message)
                client = scope.get("client", ("-", "-"))
                if client:
                    caller = f"{client[0]}:{client[1]}"
                else:
                    caller = "-:-"
                method = f"{scope.get('method', '-')} {scope.get('path', '-')}"
                status = f"{message.get('status', '-')}"
                length = f"{response_headers.get('content-length', default='-')}"
                self.logger.info(f"{caller} - {method} HTTP{status} {length}")

            await send(message)

        await self.app(scope, receive, handle_outgoing_request)
