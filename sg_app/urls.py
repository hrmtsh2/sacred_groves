from django.contrib import admin 
from django.urls import path 
from sg_app import views

urlpatterns = [
    path ("", views.index, name ='home'),
 ]