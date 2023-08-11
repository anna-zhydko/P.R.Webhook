from django.contrib import admin
from .models import PullRequest

# Register your models here.


class PullRequestAdmin(admin.ModelAdmin):
    list_display = ["number", "title", "author", "link", "updated_at", "review_requested"]


admin.site.register(PullRequest, PullRequestAdmin)
