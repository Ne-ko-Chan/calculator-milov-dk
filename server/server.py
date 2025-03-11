import subprocess
import json
import http.server as server
from urllib.parse import ParseResult, parse_qsl, urlparse
from http import HTTPStatus


# CALCULATOR WRAPPER
def calculate(expr: str, isFloat):
    command = ["build/app.exe"]
    if isFloat:
        command.append("--float")
    res = subprocess.run(
        command, input=expr, text=True, capture_output=True
    )

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
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        try:
            isFloat = self.parseRequest(body)
        except Exception as e:
            self.writeError(e.args[0],e.args[1])
            return

        try:
            res = calculate(self.calcInput, isFloat)
        except Exception as e:
            code, msg = self.calcError(e.args[0])
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
                return (HTTPStatus.BAD_REQUEST, "stack corrupted during evaluation: expression is incorrect")
            case -4:
                return (HTTPStatus.BAD_REQUEST, "input must not be empty")
            case -5:
                return (HTTPStatus.BAD_REQUEST, "null division happened during evaluation")
            case -6:
                return (HTTPStatus.BAD_REQUEST, "too many operands, expression is not correct")
            case -7:
                return (HTTPStatus.BAD_REQUEST, "wrong order, expression is incorrect")
            case _:
                return (HTTPStatus.INTERNAL_SERVER_ERROR, "unknown calculator error")

    def handle404(self):
        self.writeError(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self):
        self.parsed = urlparse(self.path)
        self.routeHandlers().get(self.parsed.path, self.handle404)()

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

    print("Listening on port 8000...")
    httpd.serve_forever()


def main():
    run()


if __name__ == "__main__":
    main()
