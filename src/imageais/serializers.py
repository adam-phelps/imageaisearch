from rest_framework import serializers
from .models import ImageFaceAnalysis, ImageObject

class ImageFaceAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFaceAnalysis
        fields = '__all__'

class ImageObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageObject
        fields = '__all__'