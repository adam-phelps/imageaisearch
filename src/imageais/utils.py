import logging
import json
import time
import boto3
import os

from .models import UploadedImage, ImageFaceAnalysis
from .serializers import ImageFaceAnalysisSerializer
from django.conf import settings


logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
b3_sts = boto3.client("sts")
deploy_region = str(b3_sts.meta.region_name)
b3_rek = boto3.client('rekognition', region_name=deploy_region)

def get_uploaded_image_location(id):
    img = UploadedImage.objects.get(id=id)
    return ('/media/imgs/' + os.path.basename(img.image.name))

def process_image(id, operations="default"):
    img = UploadedImage.objects.get(id=id)
    img_filename = settings.MEDIA_ROOT + '/imgs/' + os.path.basename(img.image.name)
    operation_results = {}
    if operations != "default":
        if operations['person_analysis'] == True:
            jsonResult = {'detect_faces_result': aws_rek_detect_faces(img_filename, img.id)}
            operations_results = operation_results.update(jsonResult)
        if operations['object_analysis'] == True:
            jsonResult = {'detect_labels_result': aws_rek_detect_labels(img_filename, img.id)}
            operation_results.update(jsonResult)
    else:
        jsonResult = {'detect_faces_result': aws_rek_detect_faces(img_filename, img.id)}
        operations_results = operation_results.update(jsonResult)

    return operation_results


def aws_rek_detect_faces(img_filename, img_id, s3bucket=False):
    json_serialized_response = []
    if s3bucket == False:
        img_instance = UploadedImage.objects.get(id=img_id)
        with open(img_filename, 'rb') as img:
            response = b3_rek.detect_faces(Image={'Bytes': img.read()}, Attributes=['ALL'])
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
        output_file = str(img_id)+'-detect_labels.json'
        with open(img_filename, 'rb') as img:
            response = b3_rek.detect_labels(Image={'Bytes': img.read()}, MaxLabels=15)
        with open(output_file, 'w') as json_out:
            json_out.write(json.dumps(response, indent=4, sort_keys=True))
        print(response)