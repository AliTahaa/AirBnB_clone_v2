#!/usr/bin/python3
""" Fabric script based on the file """

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """distributes archive to the web servers"""
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
