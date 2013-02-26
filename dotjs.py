#!/usr/bin/env python
"~/.js (python version)"
# github.com/kasun/YapDi
import yapdi
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import ssl
import sys
import os

JSDIR = os.path.join(os.path.expanduser('~'), '.js')


def get_cert():
    return """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDeJzZroDQ+ybdu
sA9fI+OUuoGz4K68rSSZxGCN7WGSzqhnWYOyXO/Sdv9hkR3C4dGQYSkVjTCEO9tD
0RsWE/5XuP2WJE94CkE0U8gpFPn2Jx/n88o0I+OZkE6RouSZCJFRkXS0T1J5Pix6
p0qCyssBY6d/OBZaZ1Vwv7gdLuUq52ykwYdf5mlsY2dNvHIdx+QCqIjTuswKbJMs
qa+9TpanWRjSztSi+Xmu5bDUXHbStJIa40zW9Ju1zQCACqyan8ANmdRzTFX+GtoI
FcK8MmU8KuP0o314uN5aHLioarCAPO7EnCqh7PTH/7mcUKxzHcpo39p3DG+3YvTS
ILXOjyCNAgMBAAECggEBALe5RlCMFak3ufRYtt3AGJ8P/+R7lQeFShfBSPkXsPJw
5uVSKpCAO/abY2mVUj+x8lathATG17EEr7nOXdBMiLST0WUycmacVICqKYeQSYlB
oil6fWfRppGBvvjC9rt5UnVbDmFwmIyc1rw5Tm4MuQdVG1kjUZlCjG7Kn8HC3tQz
NjR9eeRm8vrf5XmKmRrMAuHH5lO7N75X4JVPSew/MdranYDU0xNbPsbUQEMfcfN2
DHRnqVOtWku/2d3a5sfdN4vaRY4prJOCFLxKqXQfFXczZdBoiP1HhuK4iu3iRWgY
Ax1boMyXn/QpOEgWmLRMHdEff2kniD/xCYTDjPxX+QECgYEA8R7HrB+TUFvgzLtx
99Q1AZ2bAtCQBXG8io3sokz/ijhQAcEf1vzkqHrGAFbAnkKoNRg1ATNAy+VpUjkn
gXscuEZyZKlndXL4riYabNNLV9IJlAfFPZ3k3MpedrtYSj+xn815s1aNykzNIS92
CfIVE3r9x62Ql7VxsFZwjKBuZ5UCgYEA69zKcVQLfxP5D6nUzLX+z+PZdDKxznLT
73fIIJ4GSCA7Cp8Hp/MFgPlj3A+Tz7UAw2/JjMRHtzXL+zhRN5RTw04A7RW78SUU
dDZ5XMrl36BF+ox74sxaitPMZoxQsWWzMf72VzaMtuBFA5R/MGBwlAcssrtlA7DP
VCy6sePuNxkCgYBeztSCOHQrL8VHmxin8tfYx8jQpYNLsLoK3N1Dv/Tmu1eyKObF
GPEr0gKS1YmtcNZE8jy9ORLsWUs9Wl3PSsIzLvgB3p5gjxF7IF5ZlgdVA7BidV+3
56K6shPMqcOAhmToSdnli037UpGBz/Cg3oAtBbpNzlBBZsXKKWLd2KMwtQKBgQCX
pdD/xpLRtOzI9l/c8xMPZScWP9X0r/22FSS2XAQb8aUkchWBFY6vWymqftWBkZYZ
ElHbUQPvNwac0pvdiV/FzexogzXgmP+qrK+hSs871hfIPPUWYF/CrOTZ9lOXi5UI
iy6l6mvU1SNqZtrUJt2bP3WswTH0ioTzUQMEh1FNWQKBgFtng/DDxHy/1Fr0FXGF
QOyBnGfSlXAgY9njVd55Em89rM3pyz+wYu2ODJUe0gg8gSvxlw2+2LkZys9rngiZ
gD0YVj4TjMg0YIE8U1MLNiAPmPgBrXhwrTixiHB8tEofPb3AjvqqnR5fg9Vi2cmr
sGtyz5cKI2J8M/n6yWzCOOj3
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIID9TCCAt2gAwIBAgIJAKv/J3FyKQTjMA0GCSqGSIb3DQEBBQUAMIGQMQswCQYD
VQQGEwJFRTETMBEGA1UECAwKU29tZS1TdGF0ZTEQMA4GA1UEBwwHVGFsbGlubjEU
MBIGA1UECgwLTHVzaWthcyBJTkMxDjAMBgNVBAsMBWRvdGpzMRIwEAYDVQQDDAls
b2NhbGhvc3QxIDAeBgkqhkiG9w0BCQEWEXRhbmVsQGx1c2lrYXMuY29tMB4XDTEz
MDIyNjIwMTkwOVoXDTE0MDIyNjIwMTkwOVowgZAxCzAJBgNVBAYTAkVFMRMwEQYD
VQQIDApTb21lLVN0YXRlMRAwDgYDVQQHDAdUYWxsaW5uMRQwEgYDVQQKDAtMdXNp
a2FzIElOQzEOMAwGA1UECwwFZG90anMxEjAQBgNVBAMMCWxvY2FsaG9zdDEgMB4G
CSqGSIb3DQEJARYRdGFuZWxAbHVzaWthcy5jb20wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDeJzZroDQ+ybdusA9fI+OUuoGz4K68rSSZxGCN7WGSzqhn
WYOyXO/Sdv9hkR3C4dGQYSkVjTCEO9tD0RsWE/5XuP2WJE94CkE0U8gpFPn2Jx/n
88o0I+OZkE6RouSZCJFRkXS0T1J5Pix6p0qCyssBY6d/OBZaZ1Vwv7gdLuUq52yk
wYdf5mlsY2dNvHIdx+QCqIjTuswKbJMsqa+9TpanWRjSztSi+Xmu5bDUXHbStJIa
40zW9Ju1zQCACqyan8ANmdRzTFX+GtoIFcK8MmU8KuP0o314uN5aHLioarCAPO7E
nCqh7PTH/7mcUKxzHcpo39p3DG+3YvTSILXOjyCNAgMBAAGjUDBOMB0GA1UdDgQW
BBTL0gaqQAn1C6hpUWyDjmLKKpUknjAfBgNVHSMEGDAWgBTL0gaqQAn1C6hpUWyD
jmLKKpUknjAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQAJjGoRlQ+1
MxSDSiFrzLV6G9b6ut8cV9WF7I1AhfvE+qrPMsNQk8N5R8iIRU4wJ+2sMecP/Ibt
zBdfu5G5g7iXB0orqvXq080vF0Ecyi0e4MRDQUPU+7guaOQncnCEYyiFolY8dmQo
VjUTk1StNeCOK41sRQ/XAJs9GPvIMKgbgDlHYW5bEdDj1+rxhifsRPRgZPCnPGIh
CkiejtQ3E+k5KLgJPxusXyMJnHCXwtdl6yzV5CbgTImxtW8PbI1ExY6Z+It5Yaq5
G4TxZdHCZVlBEDyMdTn4SRCwR7wt2B9rpd6tm1+F0Jvgw1vBWUndVi6gHeOzHxck
TjoBRCr1lHEw
-----END CERTIFICATE-----
"""


def get_script(jsfile):
    chunks = jsfile.split('.')
    while chunks:
        filename = os.path.join(JSDIR, '.'.join(chunks))
        if os.path.exists(filename):
            return open(filename, 'r').read()
        chunks = chunks[1:]

    default = os.path.join(JSDIR, 'default.js')
    if os.path.exists(default):
        return open(default, 'r').read()

    return ''


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


def main():
    cert = os.path.join(JSDIR, 'server.pem')
    if not os.path.exists(cert):
        open(cert, 'w').write(get_cert())

    httpd = HTTPServer(('', 3131), Server)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert, server_side=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if 'test' in sys.argv:
    main()

elif 'start' in sys.argv or 'restart' in sys.argv:
    daemon = yapdi.Daemon()
    if 'restart' in sys.argv:
        retcode = daemon.restart()
    else:
        if daemon.status():
            print "already running"
            sys.exit()
        retcode = daemon.daemonize()

    if retcode == yapdi.OPERATION_SUCCESSFUL:
        main()
    else:
        print 'failed'

elif 'stop' in sys.argv:
    daemon = yapdi.Daemon()

    if not daemon.status():
        print "not running"
        sys.exit()

    retcode = daemon.kill()
    if retcode == yapdi.OPERATION_FAILED:
        print 'Failed'
else:
    print 'Usage:', os.path.basename(__file__), '[start|stop|restart|test]'
