# Generated by Django 2.1.5 on 2019-03-02 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20190227_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]