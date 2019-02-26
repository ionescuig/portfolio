from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
import os


class Project(models.Model):
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    title       = models.CharField(max_length=50, unique=True)
    slug        = models.SlugField()
    description = models.TextField(max_length=2500)
    position    = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    link_host   = models.URLField(blank=True)
    link_github = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.project.title + ' --- ' + os.path.basename(self.image.name)
        # to see the filename (path) can be used:
        # return str(self.image)


class CV(models.Model):
    document        = models.FileField(upload_to='cv/')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    visible         = models.BooleanField(default=False)


# next function does nothing. just for testing purposes.
#
# def project_pre_save_receiver(sender, instance, *args, **kwargs):
#     print('>>> ', instance.position)
#     print('>>> ', instance.title)
#     print('>>> ', instance.link_host)
#     print('>>> ', instance.link_github)
#
#
# pre_save.connect(project_pre_save_receiver, sender=Project)
