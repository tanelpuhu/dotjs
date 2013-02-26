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
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDRO4nxWOWZpox3
290zjmqmIxFjUy0jU40ZI4yBSzwtYNTt/wvElCly3xqVBJ71SRgzNF/5z7csqR4R
d3sWfjJK2bFNbaNUgAC4Zqqo1qs/cru7uJygTSZPmmN6bW0xRIeyz3bQfkV+lM76
QiZ1bF+V0dYr9tDkFy8XtsCI5AHqLlxBNpfuLEwpe2kBXEYUL/om45kC3RifYE1X
i56am/zILqUrzuxmyVMbBFD51nUFj03H4Z9bUVf31giH/rASVy2mSGlDAoIpkHIu
nv0rbo5dziTN09LzF1qas21zDqgoPqOkV52YaVQDfA7pOajzCMFGkEFoV2ol26Jv
CP7HlhxVAgMBAAECggEAc5C1Ii79sh5Bm7o+tUlGMrlP01KPreFqH6Z45rkNZesD
8OhcMZm8QwxjfEdvHP/gc/fLwwktnWdTikY6IDRXxuvyeFfETNnei/t464SWVZcj
hg3zxL6YGIOnymlCVGILqYHZmFMGQ2Ih6Cw9XcIcEX4zE1liC3maszhno7R8MkGk
4GCRVOZraatcZcjibrAeBDGFLD6adrnj6CDfQjLvQw6JTWCjxWpWOvpEqpGyMkvG
YVn/gmzdNWiOfQ3TPEnRsDBe65UtmAIw5RnwyUTeZiviMh45mSdWBbqZXpfoYXeT
eHoO8mLye24sHepuyVSEGPSapuNjUHHXWUiyxX6BCQKBgQD2LGDzwi4m7QME8zmp
sGoIYnbv823067p25es5Kh9K54Udj5H0XzSW/gNDy35qe/8aIvSXA7j5M93f+DCn
xnHsq5cs9dKpg24mj3dtuiBXdKnwu9ZQsQA1DfwuvutV0OjmrzYZnggPKdXXUpqY
+4l4G1MpsCXPYJvCSn0qGAboOwKBgQDZlap5fNuzmWhoO96EoU/OHwI2wsXeOqPE
osl9ejP0L8096x8+SNtVCJcVffXYWl0QmbwoUdmUHcnD9IZqyIdc/9OKxm6nQyq7
tQexl8REKBxEChEAeSmGr6JNrJcHwxLFkjVHhYiZNHOuq3Aj7R7BD5EyvSwdd1kV
F28aY15UrwKBgQDJ30S2QGO2eiBCu+5qcAfTzmM4jIh8E586h3soypkUxN0Ni8Gm
AzjOJYmp28NUMVDWLxoiiOP0QAtP8mh7/SlJasEzFndlmSkIKBhI/Bwve7Use+zZ
CP1hhJFsCBZWrlV/bulPgp+bR7RbuhqbH5Lw0n+VLSUkdVXls04G6eMoJwKBgFj4
WALhST0BJ64nfO+ivm08RL17m0kplTmcjuNeCsx4l2YQNHBVfkog/xZssRBMsu1M
z6F1BpEINS6JWEVlxeQDP87pIOoIDvs+JO07b6em9xfjPdyBrrdCLg2w2vjzjUN4
a4zZT2fGCN+NfodSOFcdNHQY4mcSHD0Bng6ePz5FAoGBAJZ9E7urg/SQ/75Y3Exa
gBrDhFUl7qK2/HuDqr61eq8VX9dEQeKltA3Kcsr3wGrfwQz7g5Ij3eD6/zwD8YtS
TyDGbdpNDS3/jufUFQGhBz7ahHdoZvH14AyTTRUbhXfWf4oJZcqesO5j633nFz+A
qV2WxChDoN/oO/qedLn548/U
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIDxTCCAq2gAwIBAgIJAOo00HVw8oguMA0GCSqGSIb3DQEBBQUAMHkxCzAJBgNV
BAYTAkVFMRMwEQYDVQQIDApTb21lLVN0YXRlMRAwDgYDVQQHDAdUYWxsaW5uMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQxIDAeBgkqhkiG9w0BCQEW
EXRhbmVsQGx1c2lrYXMuY29tMB4XDTEzMDIyNjE3MTYyNVoXDTE0MDIyNjE3MTYy
NVoweTELMAkGA1UEBhMCRUUxEzARBgNVBAgMClNvbWUtU3RhdGUxEDAOBgNVBAcM
B1RhbGxpbm4xITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEgMB4G
CSqGSIb3DQEJARYRdGFuZWxAbHVzaWthcy5jb20wggEiMA0GCSqGSIb3DQEBAQUA
A4IBDwAwggEKAoIBAQDRO4nxWOWZpox3290zjmqmIxFjUy0jU40ZI4yBSzwtYNTt
/wvElCly3xqVBJ71SRgzNF/5z7csqR4Rd3sWfjJK2bFNbaNUgAC4Zqqo1qs/cru7
uJygTSZPmmN6bW0xRIeyz3bQfkV+lM76QiZ1bF+V0dYr9tDkFy8XtsCI5AHqLlxB
NpfuLEwpe2kBXEYUL/om45kC3RifYE1Xi56am/zILqUrzuxmyVMbBFD51nUFj03H
4Z9bUVf31giH/rASVy2mSGlDAoIpkHIunv0rbo5dziTN09LzF1qas21zDqgoPqOk
V52YaVQDfA7pOajzCMFGkEFoV2ol26JvCP7HlhxVAgMBAAGjUDBOMB0GA1UdDgQW
BBT50d0d/4qgR/2Wm4F+Ci0WU2KvHTAfBgNVHSMEGDAWgBT50d0d/4qgR/2Wm4F+
Ci0WU2KvHTAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBvgEoJnbeQ
SCOZyXvITyBxNJDvmmU9/CGjFhId0HeQmXWxTTNmPC4kWnPfq2SPfCS4u2BuI2Bk
v+XqX60ovFZlgcgbus3LU1isIm2WIh80SNOUAEM+EpkRnYqX6a4Fz/5s30I787dA
AzJ3dBwJ57U3UW29Cwqmjtt/VGe2VFlmbNST3ntZ6r5a9l4Ne8h3ygCOXhJ/qFbw
P21fJEu/ZJ+CGneqyYdTNKYcTIgr5iwqXG8dy5znax01MdJHSZJdkHxZgw+mTwWt
UIT6vRMb0GrB5tItGPVlzxHpQwqG9AB5uZDDNCrEK/OPqPqz0v0WkA+K4kMi6qJT
kTifrhfayv8o
-----END CERTIFICATE-----
"""


def get_script(jsfile):
    jsfile = os.path.join(JSDIR, jsfile)
    if os.path.exists(jsfile):
        return open(jsfile, 'r').read()
    default = os.path.join(JSDIR, 'default.js')
    if os.path.exists(default):
        return open(default, 'r').read()
    return '// no ~/.js/ file\n'


class Server(BaseHTTPRequestHandler):
    def do_GET(request):
        """Respond to a GET request."""
        request.send_response(200)
        if request.path == '/':
            request.send_header("Content-Type", "text/plain")
            request.end_headers()
            request.wfile.write('GOTO http://bit.ly/dotjs')
            return

        request.send_header("Content-Type", "text/javascript")
        jsfile = request.path[1:]
        script = get_script(jsfile)
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
