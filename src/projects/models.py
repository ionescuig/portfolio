from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.template.defaultfilters import slugify
from django.urls import reverse
import os


class Project(models.Model):
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    title       = models.CharField(max_length=50, unique=True)
    slug        = models.SlugField()
    description = models.TextField(max_length=2500)
    position    = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    link_host   = models.URLField(blank=True)
    link_github = models.URLField(blank=True)
    technologies    = models.CharField(max_length=250, default='', blank=True)
    visible     = models.BooleanField(default=False)

    class Meta:
        ordering = ['title', ]

    def save(self, *args, **kwargs):
        if not self.id:
            # for new project
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def update_position(self, value):
        self.position += value
        self.save()

    def get_description(self):
        return self.description.splitlines()

    def get_technologies(self):
        return self.technologies.split(",")


def get_image_filename(instance, filename):
    return'projects/%s/%s' % (instance.project.slug, filename)


class Images(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.DO_NOTHING)
    image   = models.ImageField(upload_to=get_image_filename, verbose_name='Image')

    class Meta:
        verbose_name_plural = "Images"

    def get_absolute_url(self):
        return reverse('projects:image_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return self.project.title + ' --- ' + self.image.name


class CV(models.Model):
    document    = models.FileField(upload_to='cv/', verbose_name='CV')
    created     = models.DateTimeField(auto_now_add=True)
    visible     = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "CVs"

    def __str__(self):
        path, file = os.path.split(self.document.url)
        return file

    def get_absolute_url(self):
        return reverse('projects:cv_delete', kwargs={'pk': self.pk})


def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from Amazon S3 Bucket when corresponding 'Images'/'CV' object is deleted.
    """
    try:
        instance.image.delete(save=False)
    except:
        pass

    try:
        instance.document.delete(save=False)
    except:
        pass

    # """
    # Deletes file from filesystem when corresponding 'Images'/'CV' object is deleted.
    # """
    # try:
    #     filename = instance.image.path
    # except:
    #     pass
    #
    # try:
    #     filename = instance.document.path
    # except:
    #     pass
    #
    # path, file = os.path.split(filename)
    # # delete file
    # if os.path.isfile(filename):
    #     os.remove(filename)
    # # delete folder only if empty
    # if path:
    #     if not os.listdir(path):
    #         os.rmdir(path)


def auto_delete_images_on_project_delete(sender, instance, **kwargs):
    if instance.title:
        images = Images.objects.filter(project__slug__iexact=instance.slug)
        if images:
            for imag in images:
                if imag:
                    imag.delete()


def post_delete_project(sender, instance, **kwargs):
    if instance.position:
        position = instance.position
        projects = Project.objects.order_by('position').filter(position__gt=position)
        for proj in projects:
            proj.update_position(-1)


pre_delete.connect(auto_delete_images_on_project_delete, sender=Project)
post_delete.connect(auto_delete_file_on_delete, sender=CV)
post_delete.connect(post_delete_project, sender=Project)
post_delete.connect(auto_delete_file_on_delete, sender=Images)
