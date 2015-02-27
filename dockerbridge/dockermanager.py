"""
The DockerManager handles all communication with docker api and provides an API for all actions webrob need to perform
with the docker host.
"""
import docker
from docker.errors import *
import traceback
from utils import sysout


class DockerManager(object):
    @staticmethod
    def __docker_connect():
        c = docker.Client(base_url='unix://var/run/docker.sock', version='1.12', timeout=10)
        return c

    def start_container(self, user_container_name, user_data_container_name, common_data_container_name):
        try:
            c = self.__docker_connect()

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
                    sysout("Creating user container " + user_container_name)
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
                    sysout("Creating user_data container.")
                    c.create_container('knowrob/user_data', detach=True, tty=True, name=user_data_container_name,
                                       entrypoint='true')
                    c.start(user_data_container_name)

                if not common_data_exists:
                    sysout("Creating knowrob_data container.")
                    c.create_container('knowrob/knowrob_data', detach=True, name=common_data_container_name,
                                       entrypoint='true')
                    c.start(common_data_container_name)

                if not mongo_cont_exists:
                    sysout("Creating mongo container.")
                    c.create_container('busybox', detach=True, name='mongo_data', volumes=['/data/db'],
                                       entrypoint='true')
                    c.create_container('mongo', detach=True, ports=[27017], name='mongo_db')
                    c.start('mongo', port_bindings={27017: 27017}, volumes_from=['mongo_data'])

                sysout("Starting user container " + user_container_name)
                c.start(user_container_name,
                        port_bindings={9090: None},
                        links={('mongo_db', 'mongo')},
                        volumes_from=[user_data_container_name,
                                      common_data_container_name])
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            traceback.print_exc()

    def stop_container(self, user_container_name):
        try:
            c = self.__docker_connect()

            if c is not None:
                all_containers = c.containers(all=True)

                # check if containers exist:
                user_cont_exists = False

                for cont in all_containers:
                    if "/" + user_container_name in cont['Names']:
                        user_cont_exists = True

                if user_cont_exists:
                    sysout("Stopping container " + user_container_name + "...\n")
                    c.stop(user_container_name, timeout=5)

                    sysout("Removing container " + user_container_name + "...\n")
                    c.remove_container(user_container_name)
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")

    def get_container_ip(self, user_container_name):
        try:
            c = self.__docker_connect()

            if c is not None:
                inspect = c.inspect_container(user_container_name)
                return inspect['NetworkSettings']['IPAddress']
        except (APIError, DockerException), e:
            return 'error'

    def get_container_log(self, user_container_name):
        try:
            c = self.__docker_connect()
            logger = c.logs(user_container_name, stdout=True, stderr=True, stream=False, timestamps=False)
            logstr = ""
            # TODO: limit number of lines!
            # It seems for a long living container the log gets to huge.
            for line in logger:
                logstr += line
            return logstr
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            return 'error'