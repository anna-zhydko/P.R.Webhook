from django.contrib import admin
from .models import PullRequest, ReviewerRequested, TeamRequested

# Register your models here.


class PullRequestAdmin(admin.ModelAdmin):
    fields = ["number", "title", "author", "link", "updated_at", "reviewer_requested", "team_requested", "claimed"]
    list_display = ["number", "title", "author", "link", "updated_at", "reviewers_requested", "teams_requested", "claimed"]
    list_editable = ["claimed"]
    list_display_links = ["link", "number"]

    def reviewers_requested(self, reviewers_obj):
        return ",\n".join([reviewer.login for reviewer in reviewers_obj.reviewer_requested.all()])

    def teams_requested(self, teams_obj):
        return ",\n".join([team.name for team in teams_obj.team_requested.all()])


admin.site.register(PullRequest, PullRequestAdmin)
