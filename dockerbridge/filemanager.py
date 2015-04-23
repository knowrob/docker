"""
Basic file handling functions for handling data in docker data containers.
"""
import StringIO

import docker
from docker.errors import APIError
import dockerio

__author__ = 'mhorst@cs.uni-bremen.de'


def data_container_name(user_container_name):
    """
    Return the data container name for the given user_container_name
    """
    return 'data_'+user_container_name


def absolute_userpath(relative):
    """
    Return the absolute path to the given relative filepath inside the user data container
    """
    return '/home/ros/user_data/'+relative


def lft_transferpath(relative):
    """
    Return the absolute path to the given relative filename in the large file transfer container
    """
    return '/tmp/openEASE/dockerbridge/'+relative


class FileManager(object):
    """
    This class provides operations for reading and writing files from docker data containers that are not mounted to
    the own docker container (i.e. because they were created later than the own container).

    It can access and write single, small files, it can copy files and folders across the data and the lft_data
    container (which can be mounted by any docker container beforehand). Furthermore, it checks for file existence,
    creates directories, deletes files and directories and provides (optionally recursive) directory listings in an
    easily parseable format.

    Note that this class does some very ugly things to accomplish these functions, i.e. cat to stdin/out, or spawning
    a (temporary) docker container for each action. It is slower than direct file access and should be replaced by
    native docker functions (like https://github.com/docker/docker/pull/10198) when they come available. Also, some of
    the limitations and uglyness of this code comes from only having the standard busybox container as base image for
    temporary containers. For more complex functions, there should be a custom image with a more intelligent (network
    based) solution (preferably some lightweight HTTP REST interface) other than piping stdin/out and using cp and find.
    """
    def __init__(self):
        self.docker = docker.Client(base_url='unix://var/run/docker.sock', version='1.18', timeout=10)

    def fromcontainer(self, container, sourcefile, target):
        """
        Reads the sourcefile from the container and streams the contents to the target
        :param container: container to read in as string
        :param sourcefile: file to read as string
        :param target: target to stream the file's content to
        """
        self.__readfile(container, sourcefile, target)

    def tocontainer(self, container, source, targetfile, user=0):
        """
        Writes the content from the source to the targetfile inside the container
        :param container: container to write to as string
        :param source: stream to read data from
        :param targetfile: target to write the data to
        :param user: uid or username of the desired owner
        """
        self.__writefile(container, source, targetfile, user)

    def copy_with_lft(self, container, sourcefile, targetfile, user=0):
        """
        Copies the given sourcefile to the given target with a mounted data container and a large file transfer
        container
        :param container: datacontainer to mount
        :param sourcefile: file to copy to the target
        :param targetfile: target to copy the file to
        :param user: UID or user name to use for copying
        """
        # If source is a folder and target folder already exists, integrate sourcefolder in targetfolder. otherwise
        # copy. Note that copy might fail or produce unexpected results if target already exists (folder -> file results
        # in failure, file -> folder will copy the file INTO the folder)
        cp_cmd = "sh -c 'test -e "+targetfile+' && test -d '+targetfile + \
                 '&& cp -rf '+sourcefile+'/* '+targetfile+' || cp -rf '+sourcefile+' '+targetfile+"'"
        cont = self.__create_temp_lft_container(cp_cmd, container, user)
        self.__start_container(cont)
        self.__stop_and_remove(cont, True)

    def chown_lft(self, user=0, group=0):
        """
        Runs recursive chown with the given user and group on the lft helper container
        :param user: UID or username
        :param group: GID or groupname
        """
        cont = self.__create_temp_lft_container('chown -R '+str(user)+':'+str(group)+' '+lft_transferpath('.'))
        self.__start_container(cont)
        self.__stop_and_remove(cont, True)

    def exists(self, container, file):
        """
        Returns true if file exists inside the container
        :param container: container to check for file existence in
        :param file: the file to check
        """
        return 'Yep' in self.__exists(container, file)

    def mkdir(self, container, dir, parents=False, user=0):
        """
        Creates a new directory inside the container
        :param container: container to create the folder in
        :param dir: the directory to create
        :param parents: set to true if nonexisting parent directories should also be created
        :param user: uid or username of the desired owner
        """
        cont = self.__create_temp_container('mkdir '+('-p ' if parents else ' ')+dir, container, user)
        self.__start_container(cont)
        self.__stop_and_remove(cont, True)

    def rm(self, container, file, recursive=False):
        """
        Removes the given file from the container
        :param container: container to remove the file from
        :param file: the file to remove
        :param recursive: set to true if directories should be removed recursively
        """
        cont = self.__create_temp_container('rm '+('-r ' if recursive else ' ')+file, container)
        self.__start_container(cont)
        self.__stop_and_remove(cont, True)

    def listfiles(self, container, dir, recursive=True):
        """
        Returns all files found in given directory inside the container
        :param container: Name of the data container
        :param dir: Path to list the files from
        :param recursive: whether to recursively list all files including subdirectories
        :return: a string list of files
        """
        opts = ' -maxdepth 1' if not recursive else ''
        # The following string basically tests for each file 'find' returns if it is a directory, and prepends a 'd' to
        # the output of the filename. If it is something else (e.g. a normal file), it will prepend an 'f'.
        opts += ' -exec sh -c \'"\'"\'test -d {} && echo -n d || echo -n f; echo {}\'"\'"\' \;'
        find = self.__find(container, dir, opts)
        if len(find) > 0:
            del find[0]
        children = []
        if len(find) > 0:
            children = self.__filter_ls(find)
        return {'name': dir[dir.rfind("/")+1:], 'children': children, 'isdir': True}

    def __filter_ls(self, list, prefix='.'):
        result = []
        visited_subdirs = []
        for i in range(0, len(list)):
            # Here we check for the 'd' we prepended to the output of each 'find' result earlier
            isdir = list[i].startswith('d')
            # Remove the prepended letter for further actions
            entry = list[i][1:]
            # If we are leaving the currently processed directory
            if not entry.startswith(prefix):
                break
            # Continue if the current entry is a subdirectory that has already been processed.
            if len(filter(lambda s: s in entry, visited_subdirs)) > 0:
                continue
            children = []
            if isdir:
                # If this is a directory, pass the following entries recursively to this method to get the children.
                # This works because 'find' recursively enters all directories and appends the results directly under
                # each directory.
                children = self.__filter_ls(list[i+1:], entry)
                visited_subdirs.append(entry)
            name = entry[entry.rfind("/")+1:]
            result.append({'name': name, 'children': children, 'isdir': isdir})
        return result

    def __exists(self, data_container, file):
        cont = self.__create_temp_container('test -e '+file+' && echo Yep', data_container)
        outstream = self.__attach(cont, 'stdout')
        self.__start_container(cont)
        result = StringIO.StringIO()
        self.__pump(outstream, result)
        self.__stop_and_remove(cont, True)
        return result.getvalue()

    def __find(self, data_container, dir, opts):
        cont = self.__create_temp_container('sh -c \'cd '+dir+' && find .'+opts+'\'', data_container)
        outstream = self.__attach(cont, 'stdout')
        self.__start_container(cont)
        result = StringIO.StringIO()
        self.__pump(outstream, result)
        self.__stop_and_remove(cont, True)
        return result.getvalue().splitlines()

    def __readfile(self, data_container, sourcefile, targetstream):
        cont = self.__create_temp_container('cat '+sourcefile, data_container)
        outstream = self.__attach(cont, 'stdout')
        self.__start_container(cont)
        self.__pump(outstream, targetstream)
        self.__stop_and_remove(cont, True)

    def __writefile(self, data_container, sourcestream, targetfile, user=0):
        cont = self.__create_temp_container('sh -c \'cat > '+targetfile+'\'', data_container, user)
        instream = self.__attach(cont, 'stdin')
        self.__start_container(cont)
        self.__pump(sourcestream, instream)
        self.__stop_and_remove(cont)

    def __pump(self, instream, outstream):
        pump = dockerio.Pump(instream, outstream)
        while True:
            if pump.flush() is None:
                break

    def __create_temp_container(self, cmd, data_container, user=0):
        return self.docker.create_container(stdin_open=True,  image='busybox:latest', command=cmd, user=user,
                                            host_config={"LogConfig": {"Config": "", "Type": "none"},
                                                         "VolumesFrom": [data_container] })

    def __create_temp_lft_container(self, cmd, data_container=None, user=0):
        bind=lft_transferpath('')
        volumes = ['lft_data']
        if data_container is not None:
            volumes.append(data_container)
        return self.docker.create_container(stdin_open=True, image='busybox:latest', command=cmd, user=user,
                                            host_config={"LogConfig": {"Config": "", "Type": "none"},
                                                         "VolumesFrom": volumes})

    def __attach(self, container, streamtype):
        socket = self.docker.attach_socket(container, {streamtype: 1, 'stream': 1})
        stream = dockerio.Stream(socket)
        return dockerio.Demuxer(stream)

    def __start_container(self, container):
        try:
            self.docker.start(container)
        except APIError as e:
            # If any error occurs, kill the remaining container.
            self.__stop_and_remove(container)
            raise e

    def __stop_and_remove(self, container, wait=False):
        try:
            if wait:
                self.docker.wait(container, timeout=60)
        except APIError as e:
            # If any error occurs, kill the remaining container.
            self.__stop_and_remove(container)
            raise e
        self.docker.remove_container(container, False, False, True)