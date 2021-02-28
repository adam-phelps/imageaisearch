#!/bin/bash

# Set environment variables
IAIS_PROJECT_DIR=/home/${USER}/code/imageaisearch/

function set_env_vars() {
    
    IAIS_REGION=$(aws configure get region)

    # Launch virtual environment so we start Django with required packages
    source ${IAIS_PROJECT_DIR}venv_app/bin/activate

    # If we don't set this Django will assume we are in prod
    export DJANGO_ENV=dev

    # Required to start Django app server
    export DJANGO_SECRET_KEY=$(aws secretsmanager get-secret-value \
        --secret-id DJANGO_SECRET_KEY --region $IAIS_REGION --output text | grep "value" | awk -F '"' '{ print $4 }')
    # Required so django knows how to contact db
    export DJANGO_DB_CONFIG_FILE='iais_db_engine.cnf'
}


if [ "$1" == "--test" ]; then

    set_env_vars
    python ${IAIS_PROJECT_DIR}src/manage.py runserver

elif [ "$1" == "--run-db" ]; then

    # Launch the local MariaDB database in Docker
    docker-compose -f mariadb_stack.yml up

elif [ "$1" == "--create-super" ]; then

    set_env_vars
    python ${IAIS_PROJECT_DIR}src/manage.py createsuperuser

else
    echo "--test | Runs the manage.py and starts local development"
    echo "--run-db | Launches the local database REQUIRED for --test"
    echo "--create-super | Create the super user"
fi


