# Image AI Search
![Logo](Image_AI_Search_Logo.png?raw=true "Image AI Search")

Upload an image and explore hidden insights. Image AI Search allows you to run multiple analysis on an image to detect objects and their attributes. Determine age and number of people in an image or detect objects in an image.  Save your images and analysis for easy future retrieval. 

## User Interface
<img src="https://raw.githubusercontent.com/adam-phelps/imageaisearch/main/Image_AI_Search_example_result.PNG" width="300">


## Systems Architecture

Image AI Search is developed using the following key technologies:
* Infrastructure: AWS - Secrets Manager, IAM, Rekognition
* App Server: Django
* Database: MariaDB
* Security: IAM
* Development: Docker
* Primary Languages: Python, Javascript
## Distinctiveness and Complexity

Image AI Search allows customers to access an enterprise image classification AI system. All without having to train their own from a large library of training images.  This AI system training can be error prone and requires large amount of computing power and a large library of training set images for the system.  Using Image AI Search you can quickly perform image and object analysis using a system that is always getting upgraded and improved upon even while you sleep.

Past analysis can be stored and reviewed by user.  When performing analysis the user can either perform one or both analysis on the faces or objects detected in the image.  Additionally, capability is provided for customers to use the service without having to login.

### Key File Listing

**Development**

./dev_scripts/iais_dev_env_launch.sh - Collection of scripts to make Django app management easier such as turning launching DB, test server, and applying DB migrations.

**Database**

./dev_scripts/maradb_stack.yml - DB stack that brings up a MariaDB container with an Adminer container that allows direct DB SQL command access via a GUI.

iais_db_engine.cnf - Django configuration file with DB connection options.

**Application Logic**

src/imageais/admin.py - Configuration of admin for models `User` and `UploadedImage`
src/imageais/apps.py - Only one application `imageais` for this Django project
src/imageais/forms.py - Contains and image upload and user creation class
src/imageais/models.py - Contains models:
- UploadedImage - Foreign key to User, has other admin data related to image
- ImageFaceAnalysis - Key info from the AWS Rekongition API call to `detect_faces`
- ImageObject - Key info from AWS Rekognition API call to `detect_labels`
src/imageais/serializers.py - Provides classes to take models and convert to JSON format
src/imageais/urls.py - Standard routing for URLs with some regex defined paths to use public random UUID instead of images by their primary key.
src/imageais/utils.py - Core AWS connection logic, contains functions that interface with AWS Rekcognition to perform face and label(object) analysis.  Also contains other misc helper functions.
src/imageais/views.py - Routing for requests from POST/GETs, interfaces with helper functions to process requests
src/iais/settings.py - Key Changes:
- `SECRET_KEY` set to pull from environment variables
- `DATABASE_ENDPOINT` use MariaDB docker container
- `MEDIA_ROOT` change to local dir if in debug mode
## How to Run

* Git clone repo `git clone https://github.com/adam-phelps/imageaisearch.git` 
* Create a new python virtual environment in the root folder `python3 -m venv venv_app`
* Source to the environment and pip install packages 
```
source venv/bin/activate 
pip install -r requirements.txt
```
* Configure AWS by setting up the `iais_rek` account and configuring it.  Follow the steps in this script
```
./iais_dev_env_launch.sh --create-aws-user
```
* Set the MariaDB passwords by editing the `vim dev_scripts/.env_template` file
* Remove the "_template" from the end of the file so it reads as `.env`
* Set the Django configuraion file to same password `vim iais_db_engine_template.cnf`
* Remove the "_template" from the end of the file so it reas as `iais_db_engine.cnf`
* Launch the database
`docker stack deploy -c dev_scripts/mariadb_stack.yml iais_mariadb`
* Integrate the DB with Django prior to development `./iais_dev_env_launch.sh --make-migrations` 
* Create the super user `./iais_dev_env_launch.sh --create-super`
* Manually create the "AnonymousUser" in the Users table by logging in with the Super user to `http://127.0.0.1:8000/admin/`
* Open `Users` table and select "Add User" Enter in `AnonymousUser` as username and set password to 15 charactars random and select "save".
* Launch the development server `./iais_dev_env_launch.sh --test`
* Navigate to `http://127.0.0.1:8000/`

## Troubleshooting

Image AI Search relies on a few key Python packages:
* Django - Application Server
* Gunicorn - WSGI 
* Pillow - Image storage
* Boto3 - AWS integration

Also critical is the development db:
* Docker db MariaDB
* Get the docker container IP by running
* `docker ps -q | xargs docker inspect --format "{{range .NetworkSettings.Networks}}{{print .IPAddress}} {{end}}{{.Name}}"`




