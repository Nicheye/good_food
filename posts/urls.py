
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('',Lenta_View.as_view()),
    path('post',Post_View.as_view())
    
]