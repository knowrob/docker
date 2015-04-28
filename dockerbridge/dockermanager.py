"""
The DockerManager handles all communication with docker api and provides an API for all actions webrob need to perform
with the docker host.
"""
import traceback

import docker
from docker.errors import *
from filemanager import data_container_name, absolute_userpath

from utils import sysout


class DockerManager(object):
    webapp_images = None
    application_images = None

    def __init__(self):
        self.__client = docker.Client(base_url='unix://var/run/docker.sock', version='1.18', timeout=60)

    def start_common_container(self):
        try:
            self.__start_common_container__(self.__client.containers(all=True))
        except (APIError, DockerException), e:
            sysout("Error in start_common_container: " + str(e.message))
            traceback.print_exc()

    def __start_common_container__(self, all_containers):
        if self.__get_container("knowrob_data", all_containers) is None:
            sysout("Creating knowrob_data container.")
            self.__client.create_container('knowrob/knowrob_data', detach=True, name="knowrob_data", entrypoint='true')
            self.__client.start("knowrob_data")

        if self.__get_container("mongo_data", all_containers) is None:
            sysout("Creating mongo data container.")
            self.__client.create_container('busybox', detach=True, name='mongo_data', volumes=['/data/db'],
                                           entrypoint='true')

        if self.__get_container("lft_data", all_containers) is None:
            sysout("Creating large file transfer data container.")
            self.__client.create_container('busybox', detach=True, name='lft_data',
                                           volumes=['/tmp/openEASE/dockerbridge'], entrypoint='true')

        if self.__get_container("mongo_db", all_containers) is None:
            sysout("Creating mongo container.")
            self.__client.create_container('mongo', detach=True, name='mongo_db')
            self.__client.start('mongo', volumes_from=['mongo_data'])

    def start_user_container(self, application_image, user_container_name):
        try:
            all_containers = self.__client.containers(all=True)
            # Make sure common containers are up and running
            self.__start_common_container__(all_containers)
            # Stop user container if running
            self.__stop_container__(user_container_name, all_containers)

            user_home_dir = absolute_userpath('')

            sysout("Creating user container " + user_container_name)
            env = {"VIRTUAL_HOST": user_container_name,
                   "VIRTUAL_PORT": '9090',
                   "ROS_PACKAGE_PATH": ":".join([
                       "/home/ros/src",
                       "/opt/ros/hydro/share",
                       "/opt/ros/hydro/stacks",
                       user_home_dir
            ])}
            self.__client.create_container(application_image, detach=True, tty=True, environment=env,
                                           name=user_container_name)
                
            # Read links and volumes from webapp_container ENV
            inspect = self.__client.inspect_image(application_image)
            env = dict(map(lambda x: x.split("="), inspect['Config']['Env']))
            links = map(lambda x: tuple(x.split(':')), env['DOCKER_LINKS'].split(' '))
            volumes = env['DOCKER_VOLUMES'].split(' ')
            volumes.append(data_container_name(user_container_name))

            sysout("Starting user container " + user_container_name)
            self.__client.start(user_container_name,
                                port_bindings={9090: ('127.0.0.1',)},
                                links=links,
                                volumes_from=volumes)
        except Exception, e:
            sysout("Error in start_user_container: " + str(e.message))
            traceback.print_exc()

    def create_user_data_container(self, container_name):
        try:
            all_containers = self.__client.containers(all=True)
            user_data_container = data_container_name(container_name)
            if self.__get_container(user_data_container, all_containers) is None:
                sysout("Creating "+user_data_container+" container.")
                self.__client.create_container('knowrob/user_data', detach=True, tty=True, name=user_data_container,
                                               volumes=['/etc/rosauth'], entrypoint='true')
                self.__client.start(user_data_container)
                return True
        except (APIError, DockerException), e:
            sysout("Error in create_user_data_container: " + str(e.message))
            traceback.print_exc()
        return False

    def start_webapp_container(self, webapp_image):
        try:
            all_containers = self.__client.containers(all=True)
            # Make sure common containers are up and running
            self.__start_common_container__(all_containers)
            container_name = webapp_image.split('/')[1]
            # Stop user container if running
            if self.__get_container(container_name, all_containers) is None:
                sysout("Creating webapp container " + container_name + " for image " + webapp_image)
                env = {"VIRTUAL_HOST": container_name,
                       "VIRTUAL_PORT": '5000',
                       "OPEN_EASE_WEBAPP": 'true'}
                
                self.__client.create_container(webapp_image,
                                               detach=True, tty=True, stdin_open=True,
                                               environment=env,
                                               name=container_name,
                                               command='python runserver.py')
                
                # Read links and volumes from webapp_image ENV
                inspect = self.__client.inspect_image(webapp_image)
                img_env = dict(map(lambda x: x.split("="), inspect['Config']['Env']))
                links = map(lambda x: tuple(x.split(':')), img_env['DOCKER_LINKS'].split(' '))
                volumes = img_env['DOCKER_VOLUMES'].split(' ')
                volumes.append('lft_data')
                
                sysout("Running webapp container " + container_name)
                self.__client.start(container_name,
                                    port_bindings={5000: ('127.0.0.1',)},
                                    links=links,
                                    volumes_from=volumes)
        except Exception, e:
            sysout("Error in start_webapp_container: " + str(e.message))
            traceback.print_exc()

    def stop_container(self, container_name):
        try:
            self.__stop_container__(container_name, self.__client.containers(all=True))
        except (APIError, DockerException), e:
            sysout("Error in stop_container: " + str(e.message))

    def __stop_container__(self, container_name, all_containers):
        # check if containers exist:
        if self.__get_container(container_name, all_containers) is not None:
            sysout("Stopping container " + container_name + "...")
            self.__client.stop(container_name, timeout=5)

            sysout("Removing container " + container_name + "...")
            self.__client.remove_container(container_name)

    def get_container_ip(self, container_name):
        try:
            inspect = self.__client.inspect_container(container_name)
            return inspect['NetworkSettings']['IPAddress']
        except (APIError, DockerException), e:
            sysout("Error in get_container_ip: " + str(e.message) + "\n")
            return 'error'
    
    def get_application_image_names(self):
        if self.application_images != None: return self.application_images
        
        self.application_images = []
        
        try:
            all_images = self.__client.images(all=True)
            for img in self.get_named_images(all_images):
                inspect = self.__client.inspect_image(img)
                env = dict(map(lambda x: x.split("="), inspect['Config']['Env']))
                if 'OPEN_EASE_APPLICATION' in env:
                    sysout("OPEN_EASE_APPLICATION: " + str(img) + "\n")
                    self.application_images.append(img)
                
        except Exception, e:
            sysout("Error in get_application_image_names: " + str(e.message) + "\n")
        
        return self.application_images
    
    def get_webapp_image_names(self):
        if self.webapp_images != None: return self.webapp_images
        
        self.webapp_images = []
        
        try:
            all_images = self.__client.images(all=True)
            for img in self.get_named_images(all_images):
                if img in ['openease/easeapp', 'openease/login']: continue
                    
                inspect = self.__client.inspect_image(img)
                env = dict(map(lambda x: x.split("="), inspect['Config']['Env']))
                if 'OPEN_EASE_WEBAPP' in env:
                    sysout("OPEN_EASE_WEBAPP: " + str(img) + "\n")
                    self.webapp_images.append(img)
                
        except Exception, e:
            sysout("Error in get_webapp_image_names: " + str(e.message) + "\n")
        
        return self.webapp_images
    
    def get_named_images(self, all_images):
        named_images = []
        for img in all_images:
            tags = img['RepoTags']
            if len(tags)==0: continue
            tag0 = tags[0]
            if tag0 == '<none>:<none>': continue
            named_images.append(tag0.split(':')[0])
        return named_images

    def get_container_env(self, container_name, key):
        try:
            inspect = self.__client.inspect_container(container_name)
            env_list = inspect['Config']['Env']
            # Map to list of key-value pairs and convert to dict
            env = dict(map(lambda x: x.split("="), env_list))
            return env[key]
        except Exception, e:
            sysout("Error in get_container_env: " + str(e.message) + "\n")
            return 'error'
    
    def get_container_log(self, container_name):
        try:
            logger = self.__client.logs(container_name, stdout=True, stderr=True, stream=False, timestamps=False)
            logstr = ""
            # TODO: limit number of lines!
            # It seems for a long living container the log gets to huge.
            for line in logger:
                logstr += line
            return logstr
        except (APIError, DockerException), e:
            sysout("Error in get_container_log: " + str(e.message))
            return 'error'

    def container_exists(self, container_name, base_image_name=None):
        try:
            cont = self.__get_container(container_name, self.__client.containers(all=True))
            if base_image_name is None or cont is None:
                return cont is not None
            
            inspect = self.__client.inspect_container(container_name)
            image = inspect['Config']['Image']
            
            return image == base_image_name
        
        except (APIError, DockerException), e:
            sysout("Error in container_exists: " + str(e.message))
            return False

    @staticmethod
    def __get_container(container_name, all_containers):
        for cont in all_containers:
            if "/" + container_name in cont['Names']:
                return cont
        return None
