from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Reputation)
admin.site.register(models.Tag)
admin.site.register(models.Answer)
admin.site.register(models.Question)
