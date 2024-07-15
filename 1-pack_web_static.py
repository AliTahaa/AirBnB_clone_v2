#!/usr/bin/python3
""" Fabric script that generates a tgz """

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """generates a tgz archive"""
    try:
        d = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_n = "versions/web_static_{}.tgz".format(d)
        local("tar -cvzf {} web_static".format(file_n))
        return file_n
    except:
        return None
