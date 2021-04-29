# IAIS Views
# Adam Phelps 1/18/21
import logging
import uuid
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import FormImageUpload, UserCreationFormHidden
from .serializers import ImageFaceAnalysisSerializer
from .models import UploadedImage,User
from .utils import process_image

def display_img_search(request, id):
    if request.method == "POST":
        json_response = process_image(id)
        if len(json_response) >= 1:
            multiple_faces = True
        else:
            multiple_faces = False
        print(json_response[0])
        try:
            age = (int(json_response[0]['age_high']) + int(json_response[0]['age_low']))/2
            print(age)
        except:
            age = "UNKNOWN"
            emotions = "UNKNOWN"
        img = UploadedImage.objects.get(id=id)
        img_location = img.image.name
        logging.info(f"Getting image location: {img_location}")
        return redirect('index')

    elif request.method == "GET":
        img = UploadedImage.objects.get(public_id=id)
        img_location = img.image.name
        img_face_analysis = img.face_analysis.all()
        print(img_face_analysis)
        try:
            serializer = ImageFaceAnalysisSerializer(img_face_analysis[0])
            json_response = serializer.data
        except IndexError:
            return render(request, "imageais/result.html", {"json_response": "no_faces_detected",
                                                            "img_location": img_location})
        if len(img_face_analysis) >= 1:
            multiple_faces = True
        else:
            multiple_faces = False
        print(json_response)
        try:
            age = (int(json_response['age_high']) + int(json_response['age_low']))/2
            print(age)
        except:
            age = "UNKNOWN"
            emotions = "UNKNOWN"
        logging.info(f"Getting image location: {img_location}")
        return render(request, "imageais/result.html", {"json_response": json_response,
                                                        "img_location": img_location,
                                                        "age": age,
                                                        "multiple_faces": multiple_faces})


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
    try:
        userImg = User.objects.get(username__contains=request.user)
    except User.DoesNotExist:
        userImg = User.objects.get(username__contains="AnonymousUser")
    if request.method == "GET":
        images = UploadedImage.objects.filter(user=userImg).order_by("-timestamp")
        images_pag = Paginator(images, 10)
        try:
            page_obj = images_pag.page(request.GET['page'])
        except:
            page_obj = images_pag.page(1)
    return render(request, "imageais/images.html", {'images_page_obj': page_obj} )


def index(request):
    if request.method == 'POST':
        try:
            userImg = User.objects.get(username__contains=request.user)
        except User.DoesNotExist:
            userImg = User.objects.get(username__contains="AnonymousUser")
        print(userImg)
        form = FormImageUpload(request.POST, request.FILES)
        if form.is_valid():
            new_image = UploadedImage(user=userImg,
            public_id = uuid.uuid4(),
            image=request.FILES['file'])
            new_image.save()
            process_image(new_image.id)
            return redirect('displayimgsearch', id=str(new_image.public_id))
    else:
        form = FormImageUpload()
    return render(request, "imageais/index.html", {"form_image_upload":form})