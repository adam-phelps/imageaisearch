# Image AI Search
![Logo](Image_AI_Search_Logo.png?raw=true "Image AI Search")

Upload an image and explore hidden insights. Image AI Search allows you to run multiple analysis on an image to detect objects and their attributes. Determine age and number of people in an image or detect objects in an image.  Save your images and analysis for easy future retrieval. 

## User Interface
<img src="https://raw.githubusercontent.com/adam-phelps/imageaisearch/main/Image_AI_Search_example_result.PNG" width="300">


## Systems Architecture

Image AI Search is developed using the following key technologies:
* Infrastructure: AWS - EC2, S3, CloudFormation, CDK, SSM, Secrets Manager, Route 53, ELB/NLB, IAM, VPC
* Web Server: NGINX
* App Server: Django
* Database: MariaDB
* Security: IAM
* Development: Docker
* CI/CD: CDK/Bash
* Primary Languages: Python, Javascript

## Development

* Git clone repo
* Create a new python virtual environment in the root folder `python3 -m venv venv`
* Source to the environment and pip install packages `source venv/bin/activate` `pip install -r requirements.txt`
* Launch the docker compose file (bring up database)
* Manually create the "AnonymousUser" as user 0 in SQL db

## Troubleshooting

Image AI Search relies on a few key Python packages:
* Django
* Gunicorn
* Pillow

Also critical is the development db:
* Docker db MariaDB

## Desing Principles (Adherance to Well Architected Framework)

### 1. Operational Excellence
Changes to production resources are made via scripts (bash) and via CDK/Cloudformation updates to rollback in case of error.

Deploying Image AI search with the monitoring/canary stack allows quick notification if the web server goes offline.

### 2. Security
Image AI Search uses https with termination completed on the EC2 host.  Security is applied in depth as IAM roles instead of access keys are used to give the application access.

### 3. Reliability
Use of NLB allows multiple web servers to be added to this configuration.  Using AWS allows a scaling in RDS instance if needed.

### 4. Performance Efficiency
Instead of hosting local AI image processing software AWS Rekcognition is used to ensure this application is receiving the latest AI technology for use in processing.

### 5. Cost Optimization
Use of CDK and Cloudformation allow the environment to be destroyed and rebuilt quickly.

