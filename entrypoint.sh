#!/bin/bash

# Obtain SSL certificates using Certbot
certbot certonly --standalone --non-interactive --agree-tos --email josue@josue.codes -d cert.josue.codes -d www.cert.josue.codes

# Set up a cron job for automatic certificate renewal
echo "0 2 * * * root certbot renew --post-hook 'kill -HUP 1' > /proc/1/fd/1 2>/proc/1/fd/2" > /etc/cron.d/certbot-renew
chmod 0644 /etc/cron.d/certbot-renew
cron

# Start the Uvicorn server
python main.py
