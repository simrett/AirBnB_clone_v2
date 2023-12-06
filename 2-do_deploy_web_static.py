#!/usr/bin/python3
""" Refactor Fabric script for creating and distributing archives to web servers via the 'deploy' function.
 """

from fabric.api import env, put, run, local
from os.path import exists
import time

env.hosts = ['34.227.92.219', '54.236.50.82']

def do_pack():
    """ Packing the directory to create .tgz file """
    stime = time.strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    local("tar -cvzf versions/web_static_{}.tgz web_static/".format(stime))
    return ("versions/web_static_{}.tgz".format(stime))


def do_deploy(archive_path):
    """ distributes an archive to my web servers """
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """ Creates and deploys the web_static archive """
    archived = do_pack()
    if not archived:
        return False
    return do_deploy(archived)
