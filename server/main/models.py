from django.db import models

# Create your models here.


class PullRequest(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    link = models.CharField(max_length=200, unique=True)
    updated_at = models.CharField(max_length=100)
    review_requested = models.TextField()
    claimed = models.CharField(max_length=200, blank=True, default="")
