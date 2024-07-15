#!/usr/bin/env bash
# sets up web servers for the deployment of web_static

apt-get update
apt-get upgrade
apt-get -y install nginx
mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "Hello world" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
sed -i '/^}$/i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
service nginx start
