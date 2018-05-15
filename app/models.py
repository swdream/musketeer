from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=220)
    TYPES = (
        ('Technical', 'technical'),
        ('Myself', 'myself'),
        )
    CATEGORIES = (
        ('Devops', 'devops'),
        ('Sysadmin', 'sysadmin'),
        ('Developer', 'developer'),
	('Myself', 'myself')
        )
    STATUS = (
        ('Draft', 'Draft'),
        ('Finished', 'Finished'),
        )
    post_type = models.CharField(max_length=20, null=True, choices=TYPES)
    category = models.CharField(max_length=20, null=True, choices=CATEGORIES)
    pub_date = models.DateTimeField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True,
                                       default=timezone.datetime.now)
    images = models.ImageField(upload_to='images')
    post_content = models.TextField()
    status = models.CharField(max_length=20, null=True, choices=STATUS)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('app.Post', related_name='comments',
                             on_delete=models.deletion.CASCADE)
    author = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
