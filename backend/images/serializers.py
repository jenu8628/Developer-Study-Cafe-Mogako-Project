from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    uploaded_image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Image
        fields = ('uploaded_image',)
