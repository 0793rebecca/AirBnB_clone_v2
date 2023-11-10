#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy.
"""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
from os import path

# Set the username and SSH key
env.user = 'your_username'
env.key_filename = '/path/to/your/private/key'

# Set the list of web servers
env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if successful, None otherwise.
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Create the archive filename
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )

        # Compress the web_static folder into the archive
        local("tar -czvf versions/{} web_static".format(archive_name))

        # Return the archive path
        return path.join("versions", archive_name)

    except Exception as e:
        # Print an error message if an exception occurs
        print("Error: {}".format(e))
        return None


    def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    Args:
        archive_path: Path to the archive to deploy.

    Returns:
        True if all operations have been done correctly, otherwise returns False.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split("/")[-1]
        folder_name = archive_filename.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(folder_name)
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, remote_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -f /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        # linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
        run("ln -s {} /data/web_static/current".format(remote_path))

        return True

    except Exception as e:
        # Print an error message if an exception occurs
        print("Error: {}".format(e))
        return False

# Uncomment the lines below if you want to run the scripts locally for testing
# archive_path = do_pack()
# do_deploy(archive_path)
