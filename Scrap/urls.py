from django.contrib import admin
from django.urls import path
from Scrap import views

urlpatterns = [
    path("",views.index,name="home"),
    path("scrapper",views.scrapper,name="scrapper")
]
