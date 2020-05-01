from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('vote/', views.vote, name='vote'),
    path('create/<int:pk>', views.create, name='create'),
    path('seal', views.seal, name='seal'),
    path('verify', views.verify, name='verify'),
]