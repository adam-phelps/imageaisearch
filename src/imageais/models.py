from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class UploadedImage(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='imgs/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image} uploaded by {self.user.username}"
