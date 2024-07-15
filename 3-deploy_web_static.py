#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_n = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_n))
        return file_n
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_e = file_n.split(".")[0]
        p = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(p, no_e))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, p, no_e))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(p, no_e))
        run('rm -rf {}{}/web_static'.format(p, no_e))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(p, no_e))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    arch_path = do_pack()
    if arch_path is None:
        return False
    return do_deploy(arch_path)
