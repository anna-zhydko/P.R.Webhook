from django.db import models

# Create your models here.


class PullRequest(models.Model):
    number = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    updated_at = models.CharField(max_length=100)
    review_requested = models.TextField()
