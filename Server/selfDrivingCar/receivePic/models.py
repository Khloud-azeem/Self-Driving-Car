from django.db import models

# Create your models here.
class file(models.Model):
    path=models.CharField(max_length=1000)
class Letter(models.Model):
    Letter=models.CharField(max_length=10)
class Direction(models.Model):
    direction=models.CharField(max_length=10)
class ScannedNum(models.Model):
    scannedNum=models.CharField(max_length=10)
class Mode(models.Model):
    mode=models.CharField(max_length=10)