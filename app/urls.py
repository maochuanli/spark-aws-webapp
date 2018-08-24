from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('upload', views.upload_file, name='upload_file'),
]