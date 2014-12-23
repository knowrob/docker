import os.path
import traceback
from requests import ConnectionError

import docker
from docker.errors import *
import pyjsonrpc


def docker_connect():
    c = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
    return c


class DockerBridge(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def start_container(self, user_container_name, user_data_container_name, common_data_container_name):

        try:
            c = docker_connect()

            if c is not None:

                all_containers = c.containers(all=True)

                # check if containers exist:
                user_cont_exists = False
                user_data_cont_exists = False
                common_data_exists = False
                mongo_cont_exists = False

                for cont in all_containers:
                    if "/" + user_container_name in cont['Names']:
                        user_cont_exists = True
                    if "/" + user_data_container_name in cont['Names']:
                        user_data_cont_exists = True
                    if "/" + common_data_container_name in cont['Names']:
                        common_data_exists = True
                    if "/mongo_db" in cont['Names']:
                        mongo_cont_exists = True

                # Create containers if they do not exist yet
                if not user_cont_exists:
                    env = {"VIRTUAL_HOST": user_container_name,
                           "VIRTUAL_PORT": '9090',
                           "ROS_PACKAGE_PATH": ":".join([
                               "/home/ros/src",
                               "/opt/ros/hydro/share",
                               "/opt/ros/hydro/stacks",
                               "/home/ros/user_data/" + user_container_name
                           ])}
                    c.create_container('knowrob/hydro-knowrob-daemon',
                                       detach=True,
                                       tty=True,
                                       environment=env,
                                       name=user_container_name)

                if not user_data_cont_exists:
                    c.create_container('knowrob/user_data', detach=True, tty=True, name=user_data_container_name,
                                       entrypoint='true')
                    c.start(user_data_container_name)

                if not common_data_exists:
                    c.create_container('knowrob/knowrob_data', detach=True, name=common_data_container_name,
                                       entrypoint='true')
                    c.start(name=common_data_container_name)

                if not mongo_cont_exists:
                    c.create_container('busybox', detach=True, name='mongo_data', volumes=['/data/db'],
                                       entrypoint='true')
                    c.create_container('mongo', detach=True, ports=[27017], name='mongo_db')
                    c.start('mongo', port_bindings={27017: 27017}, volumes_from=['mongo_data'])

                containerid = c.start(user_container_name,
                                      publish_all_ports=True,
                                      links={('mongo_db', 'mongo')},
                                      volumes_from=[user_data_container_name,
                                                    common_data_container_name])

                # create home directory if it does not exist yet
                user_home_dir = '/home/ros/user_data/' + user_container_name
                if not os.path.exists(user_home_dir):
                    os.makedirs(user_home_dir)
                return containerid

        except APIError, e:
            traceback.print_exc()
            return None
        except ConnectionError, e:
            return None

    @pyjsonrpc.rpcmethod
    def stop_container(self, user_container_name):

        try:
            c = docker_connect()

            if c is not None:
                all_containers = c.containers(all=True)

                # check if containers exist:
                user_cont_exists = False

                for cont in all_containers:
                    if "/" + user_container_name in cont['Names']:
                        user_cont_exists = True

                if user_cont_exists:
                    c.stop(user_container_name, timeout=5)

                    c.remove_container(user_container_name)

        except ConnectionError, e:
            traceback.print_exc()
            return None