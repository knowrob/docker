"""
Provides input validation for rpc parameters
"""
__author__ = 'mhorst@cs.uni-bremen.de'

import re


class SecurityException(Exception):
    def __init__(self, param1, illegalvalue=None):
        Exception.__init__(self)
        if illegalvalue is None:
            self.error = param1
        else:
            self.error = 'Illegal character(s) '+illegalvalue+' detected in field '+param1

    def __str__(self):
        return self.error

#disallow all characters that are not alphanumeric, underscore or dash
illegal_containername = re.compile('[^a-zA-Z0-9_\\-]+')

#disallow all characters that are uncommon in image names
illegal_imagename = re.compile('[^a-zA-Z0-9_\\-\\.:/]+')

#disallow absolute paths, parent folders, &&, ||, semicolon and spaces without preceding backslash
illegal_pathname = re.compile('(?:^/|\\.\\./|/\\.\\.|&&|\|\||;|[^\\\\] )+')


def check_containername(input, paramname):
    result = illegal_containername.search(input)
    if result:
        raise SecurityException(paramname, result.group())


def check_imagename(input, paramname):
    result = illegal_imagename.search(input)
    if result:
        raise SecurityException(paramname, result.group())


def check_pathname(input, paramname):
    result = illegal_pathname.search(input)
    if result:
        if result.group() == '/':
            raise SecurityException('The path in '+paramname+' must not start with a /')
        if re.match(result.group(), '[^\\\\] '):
            raise SecurityException('The path in '+paramname+' must not contain spaces without preceding backslash')
        raise SecurityException(paramname, result.group())
