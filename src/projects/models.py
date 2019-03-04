from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
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

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def update_position(self, value):
        self.position += value
        self.save()


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
    document        = models.FileField(upload_to='cv/')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    visible         = models.BooleanField(default=False)


def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Images` object is deleted.
    """
    if instance.image:
        path, file = os.path.split(instance.image.path)
        # delete file
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        # delete folder only if empty
        if path:
            if not os.listdir(path):
                os.rmdir(path)


def auto_delete_images_on_project_delete(sender, instance, **kwargs):
    if instance.title:
        images = Images.objects.filter(project__slug__iexact=instance.slug)
        if images:
            for imag in images:
                if imag:
                    imag.delete()


post_delete.connect(auto_delete_file_on_delete, sender=Images)
pre_delete.connect(auto_delete_images_on_project_delete, sender=Project)


# next function does nothing. just for testing purposes.

# def project_pre_save_receiver(sender, instance, *args, **kwargs):
#     position = instance.position
#     total_positions = Project.objects.all().count()
#     if position <= total_positions:
#         projects_for_update = Project.objects.filter(position__gte=position)
#         for proj in projects_for_update:
#             proj.update_position(1)
#
#
# pre_save.connect(project_pre_save_receiver, sender=Project)
