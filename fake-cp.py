from mitmproxy import http
import logging

redirect_to = b"https://ubuntu.sec600.xyz/test"

target_hosts = (
        "detectportal.firefox.com",
        "captive.apple.com",
        "connectivitycheck.gstatic.com",
        "clients3.google.com",
        "www.msftconnecttest.com",
        "www.msftncsi.com",	# ActiveWebProbeHost
        "nmcheck.gnome.org",
        "networkcheck.kde.org",
        "cloudflarecp.com",
        "neverssl.com",
        "httpforever.com",
        "ipv6.msftconnecttext.com", # pre Win10 build 1607
        "ipv6.msftncsi.com",	# ActriveWebProbeHostV6
        "131.107.255.255", 	# ActiveDnsProbeContent
        "fd3e:4f5a:5b81::1", 	# ActiveDnsProbeContentV6
        "dns.msft.mcsi.com",	# ActiveDnsProbeHost & ActiveDnsProbeHostV6
    )

def request(flow: http.HTTPFlow) -> None:
  logging.warning("*************Request for " + flow.request.url)
  if (flow.request.headers["Host"] in target_hosts):
    # I think we should never be here unless an IP address is used instead of hostname
    logging.warning("***********Hijacking (in request logic)" + flow.request.url)
    headers = [
        (b'Location',redirect_to) 
    ]
    flow.response = http.HTTPResponse.make(307, b'ABAB', headers)
  else:
    logging.warning("***********Skipping " + flow.request.url)

def response(flow: http.HTTPFlow) -> None:
  headers = [
    (b'Server',b'fake-cp'),
    (b'Content-Type',b'text/html'),
    (b'Expires',b'0'),
    (b'Cache-Control',b'no-cache, no0store, must-revalidate'),
    (b'Pragma',b'no-cache'),
    (b'Location',redirect_to)
  ]
  flow.response = http.HTTPResponse.make(302, b'0', headers)

