from django.contrib import admin
from .models import PullRequest

# Register your models here.


class PullRequestAdmin(admin.ModelAdmin):
    list_display = ["number", "title", "author", "link", "updated_at", "review_requested", "claimed"]
    list_editable = ["claimed"]
    list_display_links = ["link", "number"]


admin.site.register(PullRequest, PullRequestAdmin)
