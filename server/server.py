import subprocess
import json
import http.server as server
from urllib.parse import ParseResult, parse_qsl, urlparse
from http import HTTPStatus


# CALCULATOR WRAPPER
def calculate(expr: str, isFloat):
    if isFloat:
        res = subprocess.run(
            ["build/app.exe", "--float"], input=expr, text=True, capture_output=True
        )
    else:
        res = subprocess.run(
            ["build/app.exe"], input=expr, text=True, capture_output=True
        )

    if res.returncode != 0:
        print("ERROR!!!", res.returncode)
    try:
        if isFloat:
            return float(res.stdout)
        else:
            return int(res.stdout)
    except ValueError as e:
        raise e


# REQUEST HANDELING
class RequestHandler(server.BaseHTTPRequestHandler):
    def routeHandlers(self):
        routeHandlers = {"/calc": self.handleCalc}
        return routeHandlers

    def handleCalc(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        isFloat, err = self.parseRequest(body)
        if err != None:
            return

        res = calculate(self.calcInput, isFloat)
        self.writeJSON(HTTPStatus.OK, str(res))

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
            self.writeError(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "unsupported Content-Type header value. Only application/json is supported",
            )
            return (None, "Unsupported media")

        query = dict(parse_qsl(self.parsed.query))
        isFloat = query.get("float", "false")
        if isFloat != "true" and isFloat != "false":
            self.writeError(
                HTTPStatus.BAD_REQUEST,
                "float parameter is present, but it's value is incorrect",
            )
            return (None, "Incorrect float value")
        if isFloat == "false":
            floatMode = False
        else:
            floatMode = True

        self.calcInput = json.loads(body)
        if not isinstance(self.calcInput, str):
            self.writeError(HTTPStatus.BAD_REQUEST, "incorrect request body")
            return (None, "Incorrect request body")

        return (floatMode, None)

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
