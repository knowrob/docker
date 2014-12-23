import pyjsonrpc

from dockerbridge import DockerBridge


http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=('0.0.0.0', 5001),
    RequestHandlerClass=DockerBridge
)
print "Starting DockerBridge ..."
print "URL: http://0:0:0:0:5001"
http_server.serve_forever()