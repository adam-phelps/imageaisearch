#!/bin/bash

# Make this an appconfig/secrets call later
IAIS_REGION=$(aws configure get region)
DJANGO_SECRET_KEY=$(aws secretsmanager get-secret-value \
        --secret-id DJANGO_SECRET_KEY --region $IAIS_REGION --output text | grep "value" | awk -F '"' '{ print $4 }')
export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
LD_LIBRARY_PATH='/usr/local/lib'
cd /opt/iais/imageaisearch/src
bash -c 'export LD_LIBRARY_PATH="'$LD_LIBRARY_PATH'" && export AWS_DEFAULT_REGION='$IAIS_REGION' && DJANGO_SECRET_KEY="'$DJANGO_SECRET_KEY'" && 
/opt/iais/imageaisearch/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          iais.wsgi'
