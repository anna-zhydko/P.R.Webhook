from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import json
from django.conf import settings
import hashlib
from .models import PullRequest
from utils.common_functions import save_webhook_payload


@csrf_exempt
def handle_webhook_event(request):
    """
    Handle GitHub webhook events.

    :param request: The HTTP request object.
    :return: HTTP response with status code.
    """

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
                save_webhook_payload(payload)
                return JsonResponse({'message': 'f{event} event has been received.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
