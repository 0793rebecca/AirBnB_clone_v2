#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    A Fabric script that generates a .tgz archive from
    the contents of the web_static folder
    folder of my AirBnB Clone repo
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
        return os.path.join("versions", archive_name)

except Exception as e:
        # Print an error message if an exception occurs
        print("Error: {}".format(e))
        return None
