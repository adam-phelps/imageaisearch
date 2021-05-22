import logging
import json
import time
import boto3
import os

from .models import UploadedImage, ImageFaceAnalysis, ImageObject
from .serializers import ImageFaceAnalysisSerializer, ImageObjectSerializer
from django.conf import settings


logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
b3_sts = boto3.client("sts")
deploy_region = str(b3_sts.meta.region_name)
b3_rek = boto3.client('rekognition', region_name=deploy_region)

def get_uploaded_image_location(id, lookup_id="default"):
    if lookup_id == "default":
        img = UploadedImage.objects.get(id=id)
        return ('/media/imgs/' + os.path.basename(img.image.name))
    elif lookup_id == "public":
        img = UploadedImage.objects.get(public_id=id)
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

def retrieve_image_analysis(id, operations="default"):
    img = UploadedImage.objects.get(public_id=id)
    img_filename = settings.MEDIA_ROOT + '/imgs/' + os.path.basename(img.image.name)
    img_face_analysis = img.face_analysis.all()
    faces_detected = len(img.face_analysis.all())
    img_object_analysis = img.image_object.all()
    objects_detected = len(img.image_object.all())
    operation_results = {}
    if operations != "default":
        if operations['person_analysis'] == True:
            person_json = []
            for face in range(0, faces_detected):
                serializer = ImageFaceAnalysisSerializer(img_face_analysis[face])
                person_json.append(serializer.data)
                print(f"On run {face} updating with Json: {person_json}")
            operations_results = operation_results.update({'detect_faces_result': person_json})
        if operations['object_analysis'] == True:
            object_json = []
            for object in range(0, objects_detected):
                serializer = ImageObjectSerializer(img_object_analysis[object])
                object_json.append(serializer.data)
            operations_results = operation_results.update({'detect_labels_result':object_json})
    return operation_results


def aws_rek_detect_faces(img_filename, img_id, s3bucket=False):
    img_instance = UploadedImage.objects.get(id=img_id)
    json_serialized_response = []
    with open(img_filename, 'rb') as img:
        if s3bucket == False:
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
    img_instance = UploadedImage.objects.get(id=img_id)
    json_serialized_response = []
    with open(img_filename, 'rb') as img:
        if s3bucket == False:
            response = b3_rek.detect_labels(Image={'Bytes': img.read()}, MaxLabels=15)
            print(f"Detect labels: {len(response['Labels'])}")
            if not response == None:
                objects_detected = len(response['Labels'])
                for object in range(0, objects_detected):
                    new_image_object = ImageObject(
                        image=img_instance,
                        object_name = response['Labels'][object]['Name'],
                        object_confidence = response['Labels'][object]['Confidence'],
                        object_instances = len(response['Labels'][object]['Instances']))
                    new_image_object.save()
                    serializer = ImageObjectSerializer(new_image_object)
                    json_serialized_response.append(serializer.data)
                return json_serialized_response