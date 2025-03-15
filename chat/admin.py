from django.contrib import admin
from . import models
# Register your models here.

models_list = [models.Message, models.ChatHistory]

admin.site.register(models_list)
