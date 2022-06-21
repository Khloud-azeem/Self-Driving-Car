from django.urls import path,include
from . import views

urlpatterns = [
    path('fileUploadApi/', views.fileUploadApi.as_view(), name='postFile'),
    path('LetterUploadApi/', views.PostLetter.as_view(), name='postLetter'),
    path('GetLetter/', views.GetLetter.as_view(), name='GetLetter'),
    path('GetDirection/', views.GetDirection.as_view(), name='GetDirection'),
    path('PostDirection/', views.PostDirection.as_view(), name='PostDirection'),
    path('GetScannedNum/', views.GetScannedNum.as_view(), name='GetScannedNum'),
    path('PostScannedNum/', views.PostScannedNum.as_view(), name='PostScannedNum'),
    path('GetMode/', views.GetMode.as_view(), name='GetMode'),
    path('PostMode/', views.PostMode.as_view(), name='PostMode'),
]