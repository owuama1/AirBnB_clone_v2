#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives, using the function do_clean.
"""
from fabric.api import env, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['10.0.2.15']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            return
    except ValueError:
        return

    archives = sorted(run("ls -t versions").split())

    for arch in archives[number:]:
        run("rm versions/{}".format(arch))

    releases = sorted(run("ls -t /data/web_static/releases").split())

    for rel in releases[number:]:
        run("rm -rf /data/web_static/releases/{}".format(rel))


def deploy():
    """
    Deploy function
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive = do_pack()
    if not archive:
        return False
    deployed = do_deploy(archive)
    if not deployed:
        return False
    return deployed


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        local("mkdir -p versions")
        file_path = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S")
        )
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}'.format(archive_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_name))
        run('rm /tmp/{}'.format(archive_filename))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_name, archive_name))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_name))
        return True
    except Exception:
        return False
