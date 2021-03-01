# IAIS Views
# Adam Phelps 1/18/21
import logging
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import FormImageUpload, UserCreationFormHidden
from .models import UploadedImage,User
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


def register_view(request):
    if request.method == "POST":
        registerform = UserCreationFormHidden(request.POST)
        if registerform.is_valid():
            user = registerform.save()
            username = registerform.cleaned_data.get("username")
            password = registerform.cleaned_data.get("password1")
            login(request, user)
            return redirect('index')
    else:
        registerform = UserCreationFormHidden()
    return render(request, 'imageais/register.html', { 'registerform':registerform })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "imageais/login.html", {
                "notification": "Username/password invalid."
            })
    else:
        return render(request, "imageais/login.html")


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse("index"))


@login_required
def get_user_images(request):
    if request.method == "GET":
        images = UploadedImage.objects.all().order_by("-timestamp")
        images_pag = Paginator(images, 10)
        try:
            page_obj = images_pag.page(request.GET['page'])
        except:
            page_obj = images_pag.page(1)
    return render(request, "imageais/images.html", {'images_page_obj': page_obj} )


def index(request):
    if request.method == 'POST':
        form = FormImageUpload(request.POST, request.FILES)
        if form.is_valid():
            new_image = UploadedImage(user=User.objects.get(username__contains=request.user),
            image=request.FILES['file'])
            new_image.save()
            return redirect('displayimgsearch', id=new_image.id)
    else:
        form = FormImageUpload()
    return render(request, "imageais/index.html", {"form_image_upload":form})