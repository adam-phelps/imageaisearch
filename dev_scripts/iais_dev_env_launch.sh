#!/bin/bash
# Adam Phelps
set -x

# Set environment variables
IAIS_PROJECT_DIR="../"

function set_env_vars() {
    
    export AWS_DEFAULT_REGION="us-east-1"

    export AWS_PROFILE="iais_rek"
    
    IAIS_REGION=$(aws configure get region --profile iais_rek)

    # Launch virtual environment so we start Django with required packages
    source ${IAIS_PROJECT_DIR}venv_app/bin/activate

    # If we don't set this Django will assume we are in prod
    export DJANGO_ENV=dev

    # Required to start Django app server
    export DJANGO_SECRET_KEY=$(aws secretsmanager get-secret-value --profile iais_rek --secret-id DJANGO_SECRET_KEY --region $IAIS_REGION --output text | grep "value" | awk -F '"' '{ print $4 }')
    # Required so django knows how to contact db
    export DJANGO_DB_CONFIG_FILE=${IAIS_PROJECT_DIR}iais_db_engine.cnf
}


if [ "$1" == "--test" ]; then

    set_env_vars
    python ${IAIS_PROJECT_DIR}src/manage.py runserver

elif [ "$1" == "--run-db" ]; then

    # Launch the local MariaDB database in Docker
    docker-compose -f mariadb_stack.yml up

elif [ "$1" == "--make-migrations" ]; then

    set_env_vars
    python ${IAIS_PROJECT_DIR}src/manage.py makemigrations imageais
    sleep 1
    python ${IAIS_PROJECT_DIR}src/manage.py migrate imageais
    sleep 1
    python ${IAIS_PROJECT_DIR}src/manage.py makemigrations
    sleep 1
    python ${IAIS_PROJECT_DIR}src/manage.py migrate

elif [ "$1" == "--create-super" ]; then

    set_env_vars
    python ${IAIS_PROJECT_DIR}src/manage.py createsuperuser

elif [ "$1" == "--env-vars" ]; then

    set_env_vars
    bash -c "$2"

elif [ "$1" == "--create-aws-user" ]; then

    set_env_vars
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --output table | xargs | awk '{ print $8 }')
    if [[ $AWS_ACCOUNT_ID =~ [0-9]{12} ]]; then
        echo "Creating iais_rek user in account $AWS_ACCOUNT_ID"
        aws iam create-user --user-name iais_rek
        aws iam attach-user-policy --policy-arn arn:aws:iam::aws:policy/AdministratorAccess --user-name iais_rek
        aws iam create-access-key --user-name iais_rek
        echo "iais_rek user created.  Set up the account now using 'aws configure --profile iais_rek'"
    else
        echo "Please configure your AWS account with permissions to create users and attach policies using 'aws configure'. "
    fi
else
    echo "--test | Runs the manage.py and starts local development"
    echo "--run-db | Launches the local database REQUIRED for --test"
    echo "--make-migrations | Make DB model changes."
    echo "--create-super | Create the super user"
    echo '--env-vars | set enviornment variables only to run other commands \n
    Example: --env-vars "src/manage.py migrate my_migrations.py"'
fi


