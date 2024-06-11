#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""
from fabric.api import *
from os.path import exists
env.hosts = ['<IP web-01>', 'IP web-02']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive filename without extension
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]

        # Create directory for the new release
        run('mkdir -p /data/web_static/releases/{}'.format(archive_name))

        # Uncompress the archive to the folder
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
