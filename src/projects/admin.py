from django.contrib import admin
import os

from .models import CV, Images, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'images_count', 'user']
    list_filter = ['title', 'position', 'user']
    search_fields = ['title', 'position', 'user', 'description', 'link_host', 'link_github']
    ordering = ['position']
    readonly_fields = ('position',)
    fields = ['position', 'title', 'description', 'link_host', 'link_github', 'slug', 'user']

    def images_count(self, obj):
        queryset = Images.objects.filter(project=obj)
        count = queryset.count()
        return count

    images_count.short_description = 'Images'


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['file', 'project', 'path']
    list_filter = ['project']
    search_fields = ['project__title', 'image']
    ordering = ['project']

    def file(self, obj):
        path, file = os.path.split(obj.image.url)
        return file

    file.short_description = 'Filename'

    def path(self, obj):
        path, file = os.path.split(obj.image.url)
        return path


admin.site.register(Project, ProjectAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(CV)
