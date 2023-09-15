from main.models import PullRequest


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
    review_requested = ", ".join([reviewer['login'] for reviewer in payload["pull_request"]["requested_reviewers"]])

    obj, created = PullRequest.objects.update_or_create(
        number=number, link=link,
        defaults={"author": author, "title": title, "updated_at": updated_at, "review_requested": review_requested}
    )
    print(obj, created)
