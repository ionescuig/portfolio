# Generated by Django 2.1.5 on 2019-03-07 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20190302_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='has_images', to='projects.Project'),
        ),
    ]
