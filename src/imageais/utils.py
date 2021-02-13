import logging
import json
import time
import boto3
import os

from .models import UploadedImage
from django.conf import settings


logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Test logging')
sts = boto3.client("sts")
deploy_region = sts.meta.region_name

def process_image_json(id):
    try:
        json_file = str(id) + '.json'
        with open(json_file,'r') as json_f:
            return json.load(json_f)
    except:
        return "ERROR"


def process_image_emotion(id):
    try:
        emotion = []
        json_file = str(id) + '.json'
        while not os.path.exists(json_file):
            time.sleep(2)
        with open(json_file,'r') as json_f:
            json_loaded = json.load(json_f)
            emotion.append(json_loaded['FaceDetails'][0]['Emotions'][0]['Type'].lower())
            emotion.append(json_loaded['FaceDetails'][0]['Emotions'][1]['Type'].lower())
            return emotion
    except:
        return "ERROR"

def process_image(id):
    img = UploadedImage.objects.get(id=id)
    img_filename = settings.MEDIA_ROOT + '/imgs/' + os.path.basename(img.image.name)
    #aws_rek_detect_labels(img_filename, img.id)
    return aws_rek_detect_faces(img_filename, img.id)

def aws_rek_detect_faces(img_filename, img_id, s3bucket=False):
    if s3bucket == False:
        client = boto3.client('rekognition', region_name=deploy_region)
        output_file = str(img_id)+'.json'
        with open(img_filename, 'rb') as img:
            response = client.detect_faces(Image={'Bytes': img.read()}, Attributes=['ALL'])
            if response['FaceDetails'] == []:
                with open(output_file, 'w') as json_out:
                    json_out.write('error')
            for faceDetail in response['FaceDetails']:
                with open(output_file, 'w') as json_out:
                    json_out.write(json.dumps(response, indent=4, sort_keys=True))
        return response

def aws_rek_detect_labels(img_filename, img_id, s3bucket=False):
    if s3bucket == False:
        client = boto3.client('rekognition')
        output_file = str(img_id)+'-detect_labels.json'
        with open(img_filename, 'rb') as img:
            response = client.detect_labels(Image={'Bytes': img.read()}, MaxLabels=15)
        with open(output_file, 'w') as json_out:
            json_out.write(json.dumps(response, indent=4, sort_keys=True))