from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('hot', hot, name='hot'),  # 热点路由
    path('book/<int:bid>', book, name='book'),  # 小说详情页路由
    path('chapter/<int:cid>', chapter, name='chapter'),  # 小说详情页路由

]
