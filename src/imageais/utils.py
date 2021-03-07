import logging
import json
import time
import boto3
import os

from .models import UploadedImage, ImageFaceAnalysis
from .serializers import ImageFaceAnalysisSerializer
from django.conf import settings


logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
sts = boto3.client("sts")
deploy_region = str(sts.meta.region_name)


def process_image(id):
    img = UploadedImage.objects.get(id=id)
    img_filename = settings.MEDIA_ROOT + '/imgs/' + os.path.basename(img.image.name)
    #aws_rek_detect_labels(img_filename, img.id)
    return aws_rek_detect_faces(img_filename, img.id)


def aws_rek_detect_faces(img_filename, img_id, s3bucket=False):
    json_serialized_response = []
    if s3bucket == False:
        client = boto3.client('rekognition', region_name=deploy_region)
        output_file = str(img_id)+'.json'
        img_instance = UploadedImage.objects.get(id=img_id)
        with open(img_filename, 'rb') as img:
            response = client.detect_faces(Image={'Bytes': img.read()}, Attributes=['ALL'])
            if not response == None:
                faces_detected = len(response['FaceDetails'])
                for face in range(0, faces_detected):
                    new_face_analysis = ImageFaceAnalysis(
                        image=img_instance,
                        face_index=face,
                        faces_detected_count=faces_detected,
                        gender=response['FaceDetails'][face]['Gender']['Value'],
                        gender_confidence=response['FaceDetails'][face]['Gender']['Confidence'],
                        top_emotion=response['FaceDetails'][face]['Emotions'][0]['Type'],
                        top_emotion_confidence=response['FaceDetails'][face]['Emotions'][0]['Confidence'],
                        second_emotion=response['FaceDetails'][face]['Emotions'][1]['Type'],
                        second_emotion_confidence=response['FaceDetails'][face]['Emotions'][1]['Confidence'],
                        age_low=response['FaceDetails'][0]['AgeRange']['Low'],
                        age_high=response['FaceDetails'][0]['AgeRange']['High'])
                    new_face_analysis.save()
                    serializer = ImageFaceAnalysisSerializer(new_face_analysis)
                    json_serialized_response.append(serializer.data)
        return json_serialized_response


def aws_rek_detect_labels(img_filename, img_id, s3bucket=False):
    if s3bucket == False:
        client = boto3.client('rekognition')
        output_file = str(img_id)+'-detect_labels.json'
        with open(img_filename, 'rb') as img:
            response = client.detect_labels(Image={'Bytes': img.read()}, MaxLabels=15)
        with open(output_file, 'w') as json_out:
            json_out.write(json.dumps(response, indent=4, sort_keys=True))