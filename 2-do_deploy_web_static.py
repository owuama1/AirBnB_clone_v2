#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""
import os
from fabric.api import env, put, run
env.hosts = ['104.196.168.90', '35.196.46.172']


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        True if the deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        print("Error: Archive file not found.")
        return False

    archive_name = os.path.basename(archive_path)
    release_name = archive_name.split('.')[0]

    try:
        # Upload the archive to /tmp
        put(archive_path, '/tmp')

        # Create directory for the new release
        run('mkdir -p /data/web_static/releases/{}'.format(release_name))

        # Extract archive to the new release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, release_name))

        # Delete the archive file
        run('rm /tmp/{}'.format(archive_name))

        # Move contents of web_static directory to release directory
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(release_name, release_name))

        # Remove the now empty web_static directory
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(release_name))

        # Update the symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(release_name))

        print("Deployment successful.")
        return True

    except Exception as e:
        print("Error:", e)
        return False
