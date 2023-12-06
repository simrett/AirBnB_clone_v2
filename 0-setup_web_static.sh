#!/usr/bin/env bash
# script to install and setup nginx. also sets up web servers for the deployment of web_static
sudo apt update
sudo apt install nginx -y
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By '$HOSTNAME';
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://realsimmie.tech;
    }

    error_page 404 /404.html;
        location /404 {
            root /var/www/html;
            internal;
        }
    }" > /etc/nginx/sites-available/default
service nginx restart
