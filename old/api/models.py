# -*- coding: utf-8 -*-
import os

os.environ['PYTHONPATH'] = '/Users/vladimir/PycharmProjects/basecollector'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.contrib.auth.models import User

from django.db import models

class CategoryTarget(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        db_table = 'myadmin_categorytarget'

class Target(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryTarget)
    city = models.CharField(default='Москва', max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    site = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_busy = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    callback = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'myadmin_target'


class Phone(models.Model):
    phone = models.CharField(max_length=40, unique=True)
    target = models.ForeignKey(Target)

    class Meta:
        db_table = 'myadmin_phone'
