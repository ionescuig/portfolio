# Generated by Django 2.1.5 on 2019-03-07 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20190307_2132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-title']},
        ),
    ]