#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives, using the function do_clean.
"""

from fabric.api import env, local, run
from os.path import exists
from datetime import datetime

# Set the username and SSH key
env.user = 'your_username'
env.key_filename = '/path/to/your/private/key'

# Set the list of web servers
env.hosts = ['<IP web-01>', 'IP web-02']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number: The number of archives, including the most recent, to keep.

    Returns:
        None.
    """
    number = int(number)

    # Delete unnecessary archives in the versions folder
    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

    # Delete unnecessary archives in the /data/web_static/releases folder of both web servers
    run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number + 1))


# Uncomment the lines below if you want to run the script locally for testing
# do_clean()
