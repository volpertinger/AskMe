from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Like)
admin.site.register(models.Dislike)
admin.site.register(models.Tag)
admin.site.register(models.Answer)
admin.site.register(models.Question)
