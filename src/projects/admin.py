from django.contrib import admin

from .models import CV, Images, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'user']
    list_filter = ['title', 'position', 'user']
    search_fields = ['title', 'position', 'user', 'description', 'link_host', 'link_github']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Images)
admin.site.register(CV)
