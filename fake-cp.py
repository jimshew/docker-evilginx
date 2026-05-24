from mitmproxy import http
import logging

REDIRECT_TO = "https://ubuntu.sec600.xyz/test"

TARGET_HOSTS = {
    "detectportal.firefox.com",
    "captive.apple.com",
    "connectivitycheck.gstatic.com",
    "clients3.google.com",
    "www.msftconnecttest.com",
    "www.msftncsi.com",
    "nmcheck.gnome.org",
    "networkcheck.kde.org",
    "cloudflarecp.com",
    "neverssl.com",
    "httpforever.com",
    "ipv6.msftconnecttext.com",
    "ipv6.msftncsi.com",
    "131.107.255.255",
    "fd3e:4f5a:5b81::1",
    "dns.msft.mcsi.com",
}

def request(flow: http.HTTPFlow) -> None:
    logging.warning(f"Request for {flow.request.url}")

    host = flow.request.pretty_host

    if host in TARGET_HOSTS:
        logging.warning(f"Hijacking request for {host}")

        flow.response = http.Response.make(
            307,
            b"Redirecting...",
            {
                "Location": REDIRECT_TO,
            },
        )
    else:
        logging.warning(f"Skipping {flow.request.url}")

def response(flow: http.HTTPFlow) -> None:
    flow.response = http.Response.make(
        302,
        b"0",
        {
            "Server": "fake-cp",
            "Content-Type": "text/html",
            "Expires": "0",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Location": REDIRECT_TO,
        },
    )
