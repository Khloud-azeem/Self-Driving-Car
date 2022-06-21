from rest_framework import serializers
from rest_framework.serializers import Serializer,FileField
from .models import Letter,Direction,ScannedNum,Mode
class filePostSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']
class PostLetterserializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ('__all__')
class PostDirectionserializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('__all__')
class PostScannedNumserializer(serializers.ModelSerializer):
    class Meta:
        model = ScannedNum
        fields = ('__all__')
class PostModeserializer(serializers.ModelSerializer):
    class Meta:
        model = Mode
        fields = ('__all__')