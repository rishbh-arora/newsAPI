from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class News(models.Model):
    source = models.TextField(null=True)
    author = models.TextField(null=True)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    publishedAt = models.DateTimeField(null=True)
    content = models.TextField(null=True)

class CustomUser(AbstractUser):
    gender = (
        ("M", "M"),
        ("F", "F"),
    )

    karma = models.PositiveIntegerField(default=0)
    gender = models.CharField(choices=gender, max_length=6, null=True)
    pno = models.CharField(max_length=10, null=True)

class Bookmarks(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fk_bookmarks")
    article = models.ForeignKey(News, on_delete = models.CASCADE, related_name="fk_bookmark_news")

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fk_comments")
    article = models.ForeignKey(News, on_delete = models.CASCADE, related_name="fk_news")
    comment = models.TextField(null=False)
    timestamp = models.DateTimeField(default=timezone.now)