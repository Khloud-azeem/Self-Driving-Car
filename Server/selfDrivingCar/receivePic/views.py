from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import filePostSerializer,PostLetterserializer,PostDirectionserializer,PostScannedNumserializer,PostModeserializer
from .models import Letter, file, Direction,ScannedNum,Mode
from selfDrivingCar.settings import MEDIA_ROOT

# Create your views here.
class fileUploadApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = filePostSerializer
    def post(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        fs = FileSystemStorage()
        fs.delete("result.jpg")
        fs.save("result.jpg", file_uploaded)
        content_type = file_uploaded.content_type
        fileName = file_uploaded.name
        filePath = MEDIA_ROOT+'/'+fileName
        file.objects.create(path=filePath)
        response = "POST API and you have uploaded a {} file".format(
            content_type)

        return Response(response)

class fileUploadApi(APIView):
    permission_classes = (AllowAny,)
    serializer_class = filePostSerializer
    def post(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        fs = FileSystemStorage()
        fs.delete("result.jpg")
        fs.save("result.jpg", file_uploaded)
        content_type = file_uploaded.content_type
        fileName = file_uploaded.name
        filePath = MEDIA_ROOT+'/'+fileName
        file.objects.create(path=filePath)
        response = "POST API and you have uploaded a {} file".format(
            content_type)

        return Response(response)
class PostLetter(APIView):
    permission_classes=(AllowAny,)
    serializer_class=PostLetterserializer
    def post(self,request):
        tempserializer=PostLetterserializer(data=request.data)
        if tempserializer.is_valid():
            tempserializer.save()
            return Response({"status": "success", "data": tempserializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": tempserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class GetLetter(APIView):
    def get(self,request):
        getLetter=Letter.objects.filter().order_by('-id')[0]
        Current_Position=getLetter.Letter
        return Response (Current_Position)
class PostDirection(APIView):
    permission_classes=(AllowAny,)
    serializer_class=PostDirectionserializer
    def post(self,request):
        dirserializer=PostDirectionserializer(data=request.data)
        if dirserializer.is_valid():
            dirserializer.save()
            return Response({"status": "success", "data": dirserializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": dirserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class GetDirection(APIView):
    def get(self,request):
        getDir=Direction.objects.filter().order_by('-id')[0]
        Current_Direction=getDir.direction
        return Response (Current_Direction)
class PostScannedNum(APIView):
    permission_classes=(AllowAny,)
    serializer_class=PostScannedNumserializer
    def post(self,request):
        Scannedserializer=PostScannedNumserializer(data=request.data)
        if Scannedserializer.is_valid():
            Scannedserializer.save()
            return Response({"status": "success", "data": Scannedserializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": Scannedserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class GetScannedNum(APIView):
    def get(self,request):
        getScannedNum=ScannedNum.objects.filter().order_by('-id')[0]
        Current_ScannedNum=getScannedNum.scannedNum
        return Response (Current_ScannedNum)
class PostMode(APIView):
    permission_classes=(AllowAny,)
    serializer_class=PostModeserializer
    def post(self,request):
        Modeserializer=PostModeserializer(data=request.data)
        if Modeserializer.is_valid():
            Modeserializer.save()
            return Response({"status": "success", "data": Modeserializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": Modeserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class GetMode(APIView):
    def get(self,request):
        getMode=Mode.objects.filter().order_by('-id')[0]
        Current_Mode=getMode.mode
        return Response (Current_Mode)