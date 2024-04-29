from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)


class MessageDepartment(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department_messages')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='department_messages')
    content = models.TextField()
    date_Added = models.DateTimeField(auto_now_add=True)
    key = models.TextField(default='')

    class Meta:
        ordering = ('-date_Added',)


class MessageRegion(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='region_messages')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='region_messages')
    content = models.TextField()
    date_Added = models.DateTimeField(auto_now_add=True)
    key = models.TextField(default='')

    class Meta:
        ordering = ('-date_Added',)
