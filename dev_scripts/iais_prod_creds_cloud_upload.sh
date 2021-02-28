#!/bin/bash

if [ "$1" == "--create-secret" ]; then

    aws secretsmanager create-secret --name DJANGO_SECRET_KEY \
        --description "Django Secret Key"
        --secret-string file://iais_prod_creds.json
elif [ "$1" == "--key-update" ]; then

    aws secretsmanager put-secret-value --secret-id DJANGO_SECRET_KEY \
        --secret-string file://iais_prod_creds.json
elif [ "$1" == "--get-key" ]; then

    aws secretsmanager get-secret-value \
       --secret-id DJANGO_SECRET_KEY --output text | grep "value" | awk -F '"' '{ print $4 }'
else
    echo "--create-secret | creates the secret key holder in Secrets Manager"
    echo "--key-update | update key"
    echo "--get-key | retrieve the current key"
fi
