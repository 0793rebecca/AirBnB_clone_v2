#!/usr/bin/env bash
# Bash script for setting up web servers for the deployment of web_static

# Install Nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo chown -R ubuntu:ubuntu /data/

# Create a fake HTML file
echo "<html><head></head><body>Hello, this is a fake HTML file!</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link, delete and recreate if it exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update ownership of /data/ folder
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static {\n\talias /data/web_static/current/;\n}\n"
sudo sed -i "/server_name _;/a $nginx_alias" $nginx_config

# Restart Nginx
sudo service nginx restart
