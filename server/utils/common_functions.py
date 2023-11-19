from main.models import PullRequest, ReviewerRequested, TeamRequested


def save_webhook_payload(payload):
    """
    Save webhook payload to django model

    :param payload: The payload from webhook post request.
    """
    number = payload["pull_request"]["number"]
    author = payload["pull_request"]["user"]["login"]
    title = payload["pull_request"]["title"]
    link = payload["pull_request"]["url"]
    updated_at = payload["pull_request"]["updated_at"]

    pr, created = PullRequest.objects.update_or_create(
        number=number, link=link,
        defaults={"author": author, "title": title, "updated_at": updated_at}
    )

    reviewer_requested_list = payload["pull_request"]["requested_reviewers"]
    for reviewer in reviewer_requested_list:
        reviewer_login = reviewer["login"]
        reviewer_github_id = reviewer["id"]
        reviewer_url = reviewer["html_url"]

        reviewer_requested, obj = ReviewerRequested.objects.update_or_create(
            github_id=reviewer_github_id,
            defaults={"login": reviewer_login, "url": reviewer_url}
        )
        pr.reviewer_requested.add(reviewer_requested)

    team_requested_list = payload["pull_request"]["requested_teams"]
    for team in team_requested_list:
        team_name = team["name"]
        team_github_id = team["id"]
        team_slug = team["slug"]
        team_url = team["url"]
        team_description = team["description"]

        team_requested, obj = TeamRequested.objects.update_or_create(
            github_id=team_github_id,
            defaults={"name": team_name, "github_id": team_github_id, "slug": team_slug,
                      "url": team_url, "description": team_description}
        )
        pr.team_requested.add(team_requested)

    print(pr, created)
