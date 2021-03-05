from rest_framework import serializers
from .models import ImageFaceAnalysis

class ImageFaceAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFaceAnalysis
        fields = '__all__'