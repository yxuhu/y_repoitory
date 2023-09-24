from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('collect/<int:nid>/', collect, name='collect'),
    path('deletecollect/<int:cid>/', deletecollect, name='deletecollect'),
    path('addtalking/<int:aid>', addtalking, name='addtalking'),
    path('addanswer/<int:tid>', addanswer, name='addanswer'),
]
