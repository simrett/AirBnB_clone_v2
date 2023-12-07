#!/usr/bin/python3
""" a script to pack static content into a tarball """
from fabric.api import local
from time import strftime


def do_pack():
    """ Prepare the web_static directory by packing """
    time_name = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(time_name))

        return "versions/web_static_{}.tgz".format(time_name)

    except Exception as e:
        return None
