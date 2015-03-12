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

    def start_common_container(self):
        try:
            c = self.__docker_connect()

            if c is not None:
                self.__start_common_container__(c, c.containers(all=True))
                
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            traceback.print_exc()

    def __start_common_container__(self, c, all_containers):
        
        if not self.__container_exists__("user_data", all_containers):
            sysout("Creating user_data container.")
            c.create_container('knowrob/user_data', detach=True, tty=True, name="user_data", entrypoint='true')
            c.start("user_data")
        
        if not self.__container_exists__("knowrob_data", all_containers):
            sysout("Creating knowrob_data container.")
            c.create_container('knowrob/knowrob_data', detach=True, name="knowrob_data", entrypoint='true')
            c.start("knowrob_data")

        if not self.__container_exists__("mongo_data", all_containers):
            sysout("Creating mongo data container.")
            c.create_container('busybox', detach=True, name='mongo_data', volumes=['/data/db'], entrypoint='true')

        if not self.__container_exists__("mongo_db", all_containers):
            sysout("Creating mongo container.")
            c.create_container('mongo', detach=True, ports=[27017], name='mongo_db')
            c.start('mongo', port_bindings={27017: 27017}, volumes_from=['mongo_data'])

    def start_user_container(self, container_name, application_container, links, volumes):
        try:
            c = self.__docker_connect()

            if c is not None:
                all_containers = c.containers(all=True)
                # Make sure common containers are up and running
                self.__start_common_container__(c, all_containers)
                # Stop user container if running
                self.__stop_container__(container_name, c, all_containers)
                
                sysout("Creating user container " + container_name)
                env = {"VIRTUAL_HOST": container_name,
                       "VIRTUAL_PORT": '9090',
                       "ROS_PACKAGE_PATH": ":".join([
                            "/home/ros/src",
                            "/opt/ros/hydro/share",
                            "/opt/ros/hydro/stacks",
                            "/home/ros/user_data/" + container_name
                ])}
                c.create_container(application_container, detach=True, tty=True, environment=env, name=container_name)
                
                sysout("Starting user container " + container_name)
                c.start(container_name,
                        port_bindings={9090: None},
                        links=links,
                        volumes_from=volumes)
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            traceback.print_exc()

    def start_webapp_container(self, container_name, webapp_container, links, volumes):
        try:
            c = self.__docker_connect()

            if c is not None:
                all_containers = c.containers(all=True)
                # Make sure common containers are up and running
                self.__start_common_container__(c, all_containers)
                # Stop user container if running
                if not self.__container_exists__(container_name, all_containers):
                    sysout("Creating webapp container " + container_name)
                    env = {"VIRTUAL_HOST": container_name,
                           "VIRTUAL_PORT": '5000',
                           "OPEN_EASE_WEBAPP": 'true'}
                    c.create_container(webapp_container, 
                                       detach=True, tty=True, stdin_open=True,
                                       environment=env,
                                       name=container_name,
                                       command='python runserver.py')
                    sysout("Running webapp container " + container_name)
                    c.start(container_name,
                          port_bindings={5000: None},
                          links=links,
                          volumes_from=volumes)
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            traceback.print_exc()

    def stop_container(self, container_name):
        try:
            c = self.__docker_connect()
            if c is not None:
                self.__stop_container__(container_name, c, c.containers(all=True))
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")

    def __stop_container__(self, container_name, c, all_containers):
        # check if containers exist:
        if self.__container_exists__(container_name, all_containers):
            sysout("Stopping container " + container_name + "...\n")
            c.stop(container_name, timeout=5)

            sysout("Removing container " + container_name + "...\n")
            c.remove_container(container_name)

    def get_container_ip(self, container_name):
        try:
            c = self.__docker_connect()

            if c is not None:
                inspect = c.inspect_container(container_name)
                return inspect['NetworkSettings']['IPAddress']
        except (APIError, DockerException), e:
            return 'error'

    def get_container_log(self, container_name):
        try:
            c = self.__docker_connect()
            logger = c.logs(container_name, stdout=True, stderr=True, stream=False, timestamps=False)
            logstr = ""
            # TODO: limit number of lines!
            # It seems for a long living container the log gets to huge.
            for line in logger:
                logstr += line
            return logstr
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            return 'error'

    def container_exists(self, container_name):
        try:
            c = self.__docker_connect()
            if c is not None:
                return self.__container_exists__(container_name, c.containers(all=True))
            else:
                return False
        except (APIError, DockerException), e:
            sysout("Error:" + str(e.message) + "\n")
            return False

    def __container_exists__(self, container_name, all_containers):
        for cont in all_containers:
            if "/" + container_name in cont['Names']:
                return True
        return False
