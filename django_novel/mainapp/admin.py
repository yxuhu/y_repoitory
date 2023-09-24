from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    pass


@admin.register(Novel)
class AdminNovel(admin.ModelAdmin):
    pass


@admin.register(Chapter)
class AdminChapter(admin.ModelAdmin):
    pass
