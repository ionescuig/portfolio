from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
    title       = models.CharField(max_length=50)
    slug        = models.SlugField()
    description = models.CharField(max_length=2500)
    position    = models.IntegerField(unique=True)
    link_hot    = models.URLField(blank=True)
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


class CV(models.Model):
    document        = models.FileField(upload_to='cv/')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    visible         = models.BooleanField(default=False)
