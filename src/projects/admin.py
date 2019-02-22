from django.contrib import admin

from .models import CV, Images, Project


admin.site.register(Project)
admin.site.register(Images)
admin.site.register(CV)
