# Generated by Django 5.0.2 on 2024-04-02 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_messageregions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagedepartment',
            old_name='room',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='messageregions',
            old_name='room',
            new_name='region',
        ),
    ]