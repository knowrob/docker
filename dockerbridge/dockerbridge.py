"""
    DockerBridge daemon for knowrob/webrob

    This daemon provides control over user containers via a JSON-RPC interface on port 5001. This must run as
    privileged/root user to access docker.sock - DO NOT DO ANYTHING OTHER THAN DOCKER COMMUNICATION
    Always sanitize method parameters in methods with @pyjsonrpc.rpcmethod annotation where necessary, as they contain
    user input.
"""
import signal
import sys

import pyjsonrpc

from dockermanager import DockerManager
from timeoutmanager import TimeoutManager
from utils import sysout


class DockerBridge(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def start_user_container(self, container_name, application_container, links, volumes):
        dockermanager.start_user_container(container_name, application_container, links, volumes)
        timeout.setTimeout(container_name, 600)
    
    @pyjsonrpc.rpcmethod
    def start_webapp_container(self, container_name, webapp_container, links, volumes):
        dockermanager.start_webapp_container(container_name, webapp_container, links, volumes)

    @pyjsonrpc.rpcmethod
    def stop_container(self, user_container_name):
        dockermanager.stop_container(user_container_name)
        timeout.remove(user_container_name)

    @pyjsonrpc.rpcmethod
    def get_container_ip(self, user_container_name):
        return dockermanager.get_container_ip(user_container_name)

    @pyjsonrpc.rpcmethod
    def refresh(self, user_container_name):
        timeout.resetTimeout(user_container_name, 600)

    @pyjsonrpc.rpcmethod
    def get_container_log(self, user_container_name):
        return dockermanager.get_container_log(user_container_name)


def handler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

dockermanager = DockerManager()

sysout("Starting watchdog")
timeout = TimeoutManager(5, dockermanager.stop_container)
timeout.start()

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=('0.0.0.0', 5001),
    RequestHandlerClass=DockerBridge
)

sysout("Starting JSONRPC")
http_server.serve_forever()
