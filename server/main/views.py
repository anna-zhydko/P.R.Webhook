from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import hmac
import json
from django.conf import settings
import hashlib
import http.client as httplib
from .models import PullRequest


def saves_to_db(values_to_save):
    number = values_to_save["pull_request"]["number"]
    author = values_to_save["pull_request"]["user"]["login"]
    title = values_to_save["pull_request"]["title"]
    link = values_to_save["pull_request"]["url"]
    updated_at = values_to_save["pull_request"]["updated_at"]
    review_requested = ", ".join([reviewer['login'] for reviewer in values_to_save["pull_request"]["requested_reviewers"]])
    # TODO add requested_teams

    obj, created = PullRequest.objects.update_or_create(
        number=number, link=link,
        defaults={"author": author, "title": title, "updated_at": updated_at, "review_requested": review_requested}
    )
    print(obj, created)


def handle_webhook(event, payload):
    print('Received the {} event'.format(event))

    if payload["action"] == "review_requested":
        saves_to_db(payload)


@csrf_exempt
def hello(request):
    # # Check the X-Hub-Signature header to make sure this is a valid request.
    # github_signature = request.META['HTTP_X_HUB_SIGNATURE']
    # signature = hmac.new(settings.SECRET_KEY, request.body, hashlib.sha1)
    # expected_signature = 'sha1=' + signature.hexdigest()
    # if not hmac.compare_digest(github_signature, expected_signature):
    #     return HttpResponseForbidden('Invalid signature header')

    # Sometimes the payload comes in as the request body, sometimes it comes in
    # as a POST parameter. This will handle either case. TODO: check if it's true
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
    else:
        payload = json.loads(request.body)

    event = request.META['HTTP_X_GITHUB_EVENT']
    print(f"{event} event has been received.")

    if event == "pull_request":
        handle_webhook(event, payload)

        return HttpResponse('Webhook pull_request received', status=httplib.ACCEPTED)

    return HttpResponse()
