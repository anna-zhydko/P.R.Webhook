# Generated by Django 4.2.1 on 2023-11-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReviewerRequested",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("login", models.CharField(max_length=100)),
                ("github_id", models.IntegerField(unique=True)),
                ("url", models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamRequested",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("github_id", models.IntegerField(unique=True)),
                ("slug", models.CharField(max_length=100)),
                ("url", models.CharField(max_length=200, unique=True)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="PullRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField(unique=True)),
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=50)),
                ("link", models.CharField(max_length=200, unique=True)),
                ("updated_at", models.CharField(max_length=100)),
                ("claimed", models.CharField(blank=True, default="", max_length=200)),
                (
                    "reviewer_requested",
                    models.ManyToManyField(blank=True, to="main.reviewerrequested"),
                ),
                (
                    "team_requested",
                    models.ManyToManyField(blank=True, to="main.teamrequested"),
                ),
            ],
        ),
    ]
