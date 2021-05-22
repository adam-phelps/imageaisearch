from rest_framework import serializers
from .models import ImageFaceAnalysis, ImageObject

class ImageFaceAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFaceAnalysis
        fields = ('timestamp', 'face_index', 'gender', 'top_emotion', 'age_low', 'age_high')

class ImageObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageObject
        fields = ('timestamp', 'object_name', 'object_confidence','object_instances')