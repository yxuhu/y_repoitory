from django.contrib import admin
from userapp.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    pass
