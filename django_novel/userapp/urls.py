from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('regist/', regist, name='regist'),
    path('active/<str:userid>/', active, name='active'),
    path('book_list/', book_list, name='book_list'),  # 我的书架路由
    path('logout/', logout, name='logout'),
    path('change/', change, name='change')
]
