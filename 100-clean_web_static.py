#!/usr/bin/python3
# delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_clean(number=0):
    """Delete out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    archs = sorted(os.listdir("versions"))
    [archs.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archs]

    with cd("/data/web_static/releases"):
        archs = run("ls -tr").split()
        archs = [a for a in archs if "web_static_" in a]
        [archs.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archs]
