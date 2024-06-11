#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create the archive name with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)

    # Print message about the packing process
    print("Packing web_static to {}".format(archive_path))

    # Create the archive using the tar command
    command = "tar -cvzf {} web_static".format(archive_path)
    result = local(command, capture=True)

    # Print the result of the tar command
    print(result)

    # Check if the command was successful
    if result.failed:
        return None

    # Get the size of the archive
    archive_size = os.path.getsize(archive_path)
    
    # Print final message
    print("web_static packed: {} -> {}Bytes".format(archive_path, archive_size))
    
    return archive_path

if __name__ == "__main__":
    result = do_pack()
    if result:
        print("Archive created successfully at: {}".format(result))
    else:
        print("Failed to create archive.")
