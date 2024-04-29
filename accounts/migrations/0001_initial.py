# Generated by Django 5.0.3 on 2024-03-27 04:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, default='media/profile/default.jpg', upload_to='media/profile')),
                ('instagram_url', models.URLField(blank=True, max_length=255)),
                ('facebook_url', models.URLField(blank=True, max_length=255)),
                ('twitter_url', models.URLField(blank=True, max_length=255)),
                ('linkedin_url', models.URLField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]