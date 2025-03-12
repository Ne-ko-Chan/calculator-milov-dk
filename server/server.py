import subprocess
import logging
import structlog
import json
import http.server as server
from urllib.parse import ParseResult, parse_qsl, urlparse
from http import HTTPStatus


def logConfig():
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Set up the root logger
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicates
    for handler in rootLogger.handlers[:]:
        rootLogger.removeHandler(handler)

    # Processors for non-structlog log entries (standard logging)
    foreignPreChain = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Console handler with colored output
    consoleHandler = logging.StreamHandler()
    consoleFormatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=True),
        foreign_pre_chain=foreignPreChain,
    )
    consoleHandler.setFormatter(consoleFormatter)

    # JSON file handler
    fileHandler = logging.FileHandler("log.json")
    fileFormatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=foreignPreChain,
    )
    fileHandler.setFormatter(fileFormatter)

    # Add handlers to the root logger
    rootLogger.addHandler(consoleHandler)
    rootLogger.addHandler(fileHandler)


logConfig()
LOGGER = structlog.get_logger()


# CALCULATOR WRAPPER
def calculate(expr: str, isFloat):
    command = ["build/app.exe"]
    if isFloat:
        command.append("--float")
    try:
        res = subprocess.run(
            command, input=expr, text=True, capture_output=True, timeout=10
        )
    except TimeoutError:
        raise Exception(2)

    if res.returncode != 0:
        raise Exception(res.returncode)
    try:
        if isFloat:
            return float(res.stdout)
        else:
            return int(res.stdout)
    except ValueError:
        raise Exception(1)


# REQUEST HANDELING
class RequestHandler(server.BaseHTTPRequestHandler):
    def routeHandlers(self):
        routeHandlers = {"/calc": self.handleCalc}
        return routeHandlers

    def handleCalc(self):
        LOGGER.info("Calculation was requested")
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        try:
            isFloat = self.parseRequest(body)
        except Exception as e:
            LOGGER.error("Parsing error", error=e.args[1], statusCode=e.args[0])
            self.writeError(e.args[0], e.args[1])
            return

        try:
            res = calculate(self.calcInput, isFloat)
        except Exception as e:
            code, msg = self.calcError(e.args[0])
            LOGGER.error("Calculation error", error=msg, statusCode=code)
            self.writeError(code, msg)
            return

        self.writeJSON(HTTPStatus.OK, str(res))

    def calcError(self, code):
        print(code)
        code = code - 256
        match code:
            case -1:
                return (HTTPStatus.BAD_REQUEST, "unexpected symbol in input")
            case -2:
                return (HTTPStatus.BAD_REQUEST, "missmatched paranteses")
            case -3:
                return (
                    HTTPStatus.BAD_REQUEST,
                    "stack corrupted during evaluation: expression is incorrect",
                )
            case -4:
                return (HTTPStatus.BAD_REQUEST, "input must not be empty")
            case -5:
                return (
                    HTTPStatus.BAD_REQUEST,
                    "null division happened during evaluation",
                )
            case -6:
                return (
                    HTTPStatus.BAD_REQUEST,
                    "too many operands, expression is not correct",
                )
            case -7:
                return (HTTPStatus.BAD_REQUEST, "wrong order, expression is incorrect")
            case 2:
                return (HTTPStatus.INTERNAL_SERVER_ERROR, "evaluation took too long")
            case _:
                return (HTTPStatus.INTERNAL_SERVER_ERROR, "unknown calculator error")

    def handle404(self):
        LOGGER.error("Not found", statusCode=404, path=self.path)
        self.writeError(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self):
        self.parsed = urlparse(self.path)
        LOGGER.info(f"Incoming {self.command} request", path=self.parsed.path, query=self.parsed.query)
        self.routeHandlers().get(self.parsed.path, self.handle404)()

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        LOGGER.info(f"{self.command} request handled", statusCode=code)
    def writeError(self, status: int, message: str):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = json.dumps(
            {
                "error": message,
            }
        ).encode("utf-8")
        self.wfile.write(body)

    def writeJSON(self, status: int, obj):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = json.dumps(obj).encode("utf-8")
        self.wfile.write(body)

    def parseRequest(self, body):
        contentType = self.headers.get("Content-Type", "")
        if not contentType.startswith("application/json"):
            raise Exception(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "unsupported Content-Type header value. Only application/json is supported",
            )

        query = dict(parse_qsl(self.parsed.query))
        isFloat = query.get("float", "false")
        if isFloat != "true" and isFloat != "false":
            raise Exception(
                HTTPStatus.BAD_REQUEST,
                "float parameter is present, but it's value is incorrect",
            )
        if isFloat == "false":
            floatMode = False
        else:
            floatMode = True

        self.calcInput = json.loads(body)
        if not isinstance(self.calcInput, str):
            raise Exception(HTTPStatus.BAD_REQUEST, "incorrect request body")

        return floatMode

    parsed: ParseResult
    calcInput: str


def run(server_class=server.HTTPServer, handler_class=RequestHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)

    LOGGER.info("Started listening on port 8000")
    httpd.serve_forever()


def main():
    run()


if __name__ == "__main__":
    main()
