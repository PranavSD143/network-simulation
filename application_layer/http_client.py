from urllib.parse import urlparse

class BrowserHTTPClient:
    def __init__(self, method, url, headers=None, body=""):
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.body = body
        self._parse_url()

    def _parse_url(self):
        parsed = urlparse(self.url)
        self.scheme = parsed.scheme or "http"
        self.host = parsed.hostname
        self.port = parsed.port or (443 if self.scheme == "https" else 80)
        self.path = parsed.path or "/"
        if parsed.query:
            self.path += "?" + parsed.query

    def _build_request_line(self):
        return f"{self.method} {self.path} HTTP/1.1\r\n"

    def _build_headers(self):
        # Add required headers like a browser would
        self.headers.setdefault("Host", self.host)
        self.headers.setdefault("User-Agent", "SimulatedBrowser/1.0")
        self.headers.setdefault("Accept", "*/*")
        self.headers.setdefault("Connection", "close")

        if self.method == "POST" and self.body:
            self.headers.setdefault("Content-Type", "application/json")
            self.headers["Content-Length"] = str(len(self.body.encode()))

        return "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())

    def build_http_request_bytes(self):
        request_line = self._build_request_line()
        headers = self._build_headers()
        http_message = request_line + headers + "\r\n" + self.body
        # print(http_message)
        return http_message.encode()

    def get_host_port(self):
        return self.host, self.port
