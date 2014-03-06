#!/usr/bin/env python
"~/.js (python version)"
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ForkingMixIn
import tempfile
import ssl
import os
import re

JSDIR = os.path.join(os.path.expanduser('~'), '.js')

if not os.path.exists(JSDIR):
    os.mkdir(JSDIR)


def create_cert_file():
    filename = tempfile.mktemp('.pem', 'dotjs-')
    content = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCy3MHFXHOAhTM3
AlAy/kV+9DCbIR/An87ytC4Casn7z09EZQ4hZM3toxed7xGliJITPuytZFmUOIcU
3tpuo3eZs5248dFHsvDg4vYu2eerruJqS52X8d6J0d4Mx/yqIVYyMqzdPONssq/y
+0IonZkCg29ubPGW0CZUior1PrM+PRf59zVigXMr2KnRwYh9nYL/oYYtb7p+rqTm
zIsj2I5bh1wldQEKKA2rtRqR/Po7CRN95cpqq+qK2U2gHYNzemLhgVr9RM3uVgTx
e4GCv90TF0YlYJjdc92HbmFEX3I+wiDFIkpDfUi2OY90GizfvcSYg3zof/qVZ1y7
sBP5IxP1AgMBAAECggEAfG/fk8qFRQXmor/GQiPq/68t3c+GwsGr/ejjFaVsDvel
A0V3Nj5mkozkEmnQEiVY03D0wpFNTTSirh95Qn4R6GoxMgly+3n/4cWlVuUdK7GJ
LkCbTKnmlGXhIW1FWKvGxzfAUk9ZPjd2+ApcddtnJ3t/3AiJb84yzKBymrrbg1Fe
DBX2jN+2Dx8hpE58QOJcaSMJkvQ/GDofvviN/Ew/iUrm6idC62HYLeVcckjIGA3J
LO5jkvFVzcidHbXdnQ8w1GjLM7D+hLe38QX0/ICqZyT32me1b0LP2pcsK+ozWS3N
vlbZNYyshrSAHDykddle6e83Hmr2BWxaYGVJ7YwV5QKBgQDW8hIrIYUZCaeAfE+a
aCzaPE2oHOCfLNg8iYt3sGqn5KXNFf/+Bcs9+S42CENIBPzND8DRkCFXmQMY3xmG
mBAhc0SEx/JI/JYcr/6Uxg5QHEc+JNPAtD5Ye4InCf1IkSBTNpUSoTRilQRDIYq3
p4ib1M0ALsYoywiI9tmm9OBt/wKBgQDVBl4Q3mtJZyCtnMuZNHrjMR6dNbwQHaR7
e0voKasW8xA/xRzMsoIENnCrAyQTJiRvBSiUWA09VPG36n8o/Rkz/zuE/VlKFmrn
QgK+iYMptZobsM1YrMUqDxP7AyCpKwGfflJsWP9Uaop+8hdBaoEwRQMMXI5PITuK
TudbmdWmCwKBgF7krdq2yLDeD0HtH6OWXD7YopwWa6A6RxiqzJTBoMSQcBZToRl/
a1Pn31vhV/rCoOzTCJg8Hkwy9CgVzooaNfzei6BnOXK5eHgfxq/dpFH/ugAYeBe6
O1AK7tHXWiegUnoKPdPksWDYUvJkK36bCvdpAjwTak52HEWDXWGU+EP3AoGBALEL
rbpPYNOMxngETKJ0H34bINqAAmFSgZWvD5NQrkVQljyp0hm+cpiVtmYrIhxYIwey
PdusorRKmOrGFhE26W9xvUH2XfNZVlgFYMqC92P+7qn8822zido+1dhU7RwsBhlM
n6w0+2Bpe9mt0u4nWl+Hu9TWR+A0OovksBxNamepAoGAKmU7MUKLCsnaOvp3CwUF
a5H8y9ClzOaqpCrz6gK+q/T2cc2z82AoOjylrPWcSLPIreG9erqHsO5kne06WOBA
1XaKC6UOn+mLO/0BdLbiQayKHJVA7HToisoIQLB/FHbcah+CQXtugG2biEnWlq6x
AN6oVvTFpG8Hkonv7bMqm2A=
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIID4zCCAsugAwIBAgIJAPmw94QQhgSoMA0GCSqGSIb3DQEBBQUAMIGHMQswCQYD
VQQGEwJFRTEOMAwGA1UECAwFSGFyanUxEDAOBgNVBAcMB1RhbGxpbm4xFDASBgNV
BAoMC0x1c2lrYXMgSU5DMQ4wDAYDVQQLDAVBQkNERjEOMAwGA1UEAwwFRE9USlMx
IDAeBgkqhkiG9w0BCQEWEXRhbmVsQGx1c2lrYXMuY29tMB4XDTE0MDMwNjA3NTUy
N1oXDTMwMDgwOTA3NTUyN1owgYcxCzAJBgNVBAYTAkVFMQ4wDAYDVQQIDAVIYXJq
dTEQMA4GA1UEBwwHVGFsbGlubjEUMBIGA1UECgwLTHVzaWthcyBJTkMxDjAMBgNV
BAsMBUFCQ0RGMQ4wDAYDVQQDDAVET1RKUzEgMB4GCSqGSIb3DQEJARYRdGFuZWxA
bHVzaWthcy5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCy3MHF
XHOAhTM3AlAy/kV+9DCbIR/An87ytC4Casn7z09EZQ4hZM3toxed7xGliJITPuyt
ZFmUOIcU3tpuo3eZs5248dFHsvDg4vYu2eerruJqS52X8d6J0d4Mx/yqIVYyMqzd
PONssq/y+0IonZkCg29ubPGW0CZUior1PrM+PRf59zVigXMr2KnRwYh9nYL/oYYt
b7p+rqTmzIsj2I5bh1wldQEKKA2rtRqR/Po7CRN95cpqq+qK2U2gHYNzemLhgVr9
RM3uVgTxe4GCv90TF0YlYJjdc92HbmFEX3I+wiDFIkpDfUi2OY90GizfvcSYg3zo
f/qVZ1y7sBP5IxP1AgMBAAGjUDBOMB0GA1UdDgQWBBS/14zl9rynDhVeeeGdLDIp
sxVsJjAfBgNVHSMEGDAWgBS/14zl9rynDhVeeeGdLDIpsxVsJjAMBgNVHRMEBTAD
AQH/MA0GCSqGSIb3DQEBBQUAA4IBAQB17kzT5YeXXlTWRc8T5mMByYJ3Re1VTMVi
DJ3WYXrW6SmFXINMBPV085dsJsMwv4OpapQo1CbEhbUYRtrFFI7LQWE1/dCp1Rmf
IUjzFHreXwn7iSHeDwoOWed3aXWn4Nj/BZqZzlWPbk0fRE0ZJQvbq1n4SgtJ3Rwk
wuvk37jKuRutA3RjEghGWZTe+S3/1QBlGrZ9pc5hTcrhPNXvZXot5QuNhDegt5P6
mthY389EvYnucSEepLfnY9AXR0yGAAsjnaGMm59UUJz7GQ3CdEGftaPXf2XmquF9
fl0ON4HHyEJKa1mvinueSOX1WskLla6z64swvjbfiCgTC9gKW6tn
-----END CERTIFICATE-----
"""
    open(filename, 'w').write(content)
    return filename


def get_script(jsfile):
    content = None

    chunks = jsfile.split('.')
    while chunks:
        filename = os.path.join(JSDIR, '.'.join(chunks))
        if os.path.exists(filename):
            content = open(filename, 'r').read()
            break
        chunks = chunks[1:]

    if content is None:
        default = os.path.join(JSDIR, 'default.js')
        if not os.path.exists(default):
            return ''
        content = open(default, 'r').read()

    pattern = '//(\s*)include\s+(?P<filename>.*)$'
    for inc in re.finditer(pattern, content, re.MULTILINE):
        found = inc.group()
        name = inc.groupdict()
        filename = os.path.join(JSDIR, name.get('filename', ''))
        if os.path.exists(filename):
            content = content.replace(found, open(filename, 'r').read())

    return content


class Server(BaseHTTPRequestHandler):

    def do_GET(request):
        """Respond to a GET request."""
        request.send_response(200)
        if not request.path.endswith('.js'):
            request.send_header("Content-Type", "text/plain")
            request.end_headers()
            request.wfile.write('GOTO http://bit.ly/dotjs')
            return

        request.send_header("Content-Type", "text/javascript")
        jsfile = request.path[1:]
        script = get_script(jsfile)
        if not script:
            script = '// no ~/.js/ file\n'
        request.send_header("Content-Length", len(script))
        request.end_headers()
        request.wfile.write(script)


class ForkingHTTPServer(ForkingMixIn, HTTPServer):

    def finish_request(self, request, client_address):
        request.settimeout(30)
        HTTPServer.finish_request(self, request, client_address)


def main():
    srvr = ForkingHTTPServer(('127.0.0.1', 3131), Server)
    srvr.socket = ssl.wrap_socket(
        srvr.socket, certfile=create_cert_file(), server_side=True)
    try:
        srvr.serve_forever()
    except KeyboardInterrupt:
        srvr.socket.close()
        print 'Bye'


if __name__ == '__main__':
    main()
