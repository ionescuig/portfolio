# Generated by Django 2.1.5 on 2019-03-08 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20190307_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cv',
            old_name='created_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='cv',
            name='modified_date',
        ),
    ]
