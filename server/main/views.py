from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
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
    # Check the X-Hub-Signature header to make sure this is a valid request.
    github_signature = request.META['HTTP_X_HUB_SIGNATURE']
    secret_bytes = bytes(settings.SECRET_KEY, 'utf-8')

    signature = hmac.new(secret_bytes, request.body, hashlib.sha1)
    expected_signature = 'sha1=' + signature.hexdigest()

    if not hmac.compare_digest(github_signature, expected_signature):
        return HttpResponseForbidden('Invalid signature header')

    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode('utf-8'))
            event = request.META['HTTP_X_GITHUB_EVENT']

            if event == "pull_request":
                handle_webhook(event, payload)
                return JsonResponse({'message': 'f{event} event has been received.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
