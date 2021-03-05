from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='imgs/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image} uploaded by {self.user.username}"

class ImageFaceAnalysis(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name="face_analysis")
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(max_length=20, null=True, blank=True)
    
    #API call aws_rek_detect_faces returns FaceDetails: [{}, {}] this is that index in the JSON Response
    face_index = models.PositiveSmallIntegerField()
    faces_detected_count = models.PositiveSmallIntegerField(null=True, blank=True)

    #Face Analysis granular details
    gender = models.CharField(max_length=10, null=True, blank=True)
    gender_confidence = models.FloatField(null=True, blank=True)
    top_emotion = models.CharField(max_length=20,null=True, blank=True)
    top_emotion_confidence = models.FloatField(null=True, blank=True)
    second_emotion = models.CharField(max_length=20,null=True, blank=True)
    second_emotion_confidence = models.FloatField(null=True, blank=True)
    age_low = models.PositiveSmallIntegerField(null=True, blank=True)
    age_high = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.image} Face Analyis object ID {self.id} index {self.face_index}"

    class Meta:
        ordering = ['face_index']