# IAIS Views
# Adam Phelps 1/18/21
import logging
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .forms import FormImageUpload
from .models import UploadedImage
from .utils import process_image,process_image_json,process_image_emotion

def display_img_search(request, id):
    json_response = process_image(id)
    try:
        json_response['FaceDetails'][1]
        multiple_faces = True
    except (IndexError, TypeError):
        multiple_faces = False
    try:
        emotions = process_image_emotion(id)
        json_response['FaceDetails'][0]['Gender']['Confidence'] = round(float(json_response['FaceDetails'][0]['Gender']['Confidence']),2)
        age = (int(json_response['FaceDetails'][0]['AgeRange']['High']) + int(json_response['FaceDetails'][0]['AgeRange']['Low']))/2
        #json_response['Gender']['Confidence'] = round(float(json_response['Gender']['Confidence']),2)
        #age = (int(json_response['AgeRange']['High']) + int(json_response['AgeRange']['Low']))/2
    except:
        age = "UNKNOWN"
        emotions = "UNKNOWN"
    img = UploadedImage.objects.get(id=id)
    img_location = img.image.name
    logging.info(f"Getting image location: {img_location}")
    return render(request, "imageais/result.html", {"json_response": json_response,
                                                    "multiple_faces": multiple_faces, 
                                                    "img_location": img_location,
                                                    "top_emotion": emotions[0],
                                                    "second_emotion": emotions[1],
                                                    "age": age})

def index(request):
    if request.method == 'POST':
        form = FormImageUpload(request.POST, request.FILES)
        if form.is_valid():
            new_image = UploadedImage(image=request.FILES['file'])
            new_image.save()
            return redirect('displayimgsearch', id=new_image.id)
    else:
        form = FormImageUpload()
    return render(request, "imageais/index.html", {"form_image_upload":form})