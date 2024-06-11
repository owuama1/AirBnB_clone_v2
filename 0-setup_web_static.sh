#!/usr/bin/env bash
# Update package list and install Nginx if it's not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt update
    sudo apt install -y nginx
fi

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Welcome to your web_static test page.
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link, forcefully delete if it already exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content
sudo sed -i '/server_name _;/a \\n    location /hbnb_static {\n        alias /data/web_static/current/;\n    }' /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
sudo service nginx restart

echo "Setup completed successfully!"
