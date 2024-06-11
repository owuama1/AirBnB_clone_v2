#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy.
"""
from fabric.api import *
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    All archives are stored in the versions folder.
    The archive name is web_static_<year><month><day><hour><minute><second>.tgz.
    The function returns the archive path if the archive has been correctly
    generated, otherwise it returns None.
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        file_path = "versions/web_static_{}.tgz".format(now)
        local("tar -czvf {} web_static".format(file_path))
        return file_path
    except:
        return None


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


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
