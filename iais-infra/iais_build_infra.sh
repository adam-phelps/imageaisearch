#!/bin/bash

if [ $1 == "key-upload" ]; then
    aws secretsmanager create-secret --name DJANGO_SECRET_KEY \
        --description "Django Secret Key"
        --secret-string file://creds.json
    aws secretsmanager put-secret-value --secret-id DJANGO_SECRET_KEY \
        --secret-string file://creds.json
fi

#DJANGO_SECRET_KEY=$(aws secretsmanager get-secret-value \
#       --secret-id DJANGO_SECRET_KEY --output text | grep "value" | awk -F '"' '{ print $4 }')