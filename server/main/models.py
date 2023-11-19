from django.db import models


class ReviewerRequested(models.Model):
    login = models.CharField(max_length=100)
    github_id = models.IntegerField(unique=True)
    url = models.CharField(max_length=200, unique=True)


class TeamRequested(models.Model):
    name = models.CharField(max_length=200)
    github_id = models.IntegerField(unique=True)
    slug = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)
    description = models.TextField()


class PullRequest(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    link = models.CharField(max_length=200, unique=True)
    updated_at = models.CharField(max_length=100)
    reviewer_requested = models.ManyToManyField(ReviewerRequested, blank=True)
    team_requested = models.ManyToManyField(TeamRequested, blank=True)
    claimed = models.CharField(max_length=200, blank=True, default="")
