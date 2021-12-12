from django.contrib import admin
from subjects import models

admin.site.register(models.Subject)
admin.site.register(models.Comment)
