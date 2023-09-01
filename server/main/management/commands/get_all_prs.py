from django.core.management.base import BaseCommand, CommandError
import requests
from ...models import PullRequest


class FetchWebhookData:
    token = "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"
    owner, repo = "anna-zhydko", "django-tutorial"

    def _get_response(self, url):
        """
        Make http request to interact with GitHub CLI
        https://docs.github.com/en/github-cli/github-cli/about-github-cli

        :param url: API url to get a specific data
        :return: response in json
        """
        headers = {
            "authorization": "Bearer {}".format(self.token)
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_webhook_id(self):
        """
        Retrieve list of all webhooks for the specified repository.
        https://docs.github.com/en/free-pro-team@latest/rest/webhooks/repos?apiVersion=2022-11-28#list-repository-webhooks

        Given that the current repo has only one webhook - we take the first item in the list.

        :return: Id of the webhook
        """
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/hooks"
        list_repository_webhooks = self._get_response(url)
        return list_repository_webhooks[0]["id"]

    def get_deliveries_ids_list(self):
        """
        Retrieve a list of webhook deliveries for a webhook configured in a repository.
        https://docs.github.com/en/free-pro-team@latest/rest/webhooks/repo-deliveries?apiVersion=2022-11-28#list-deliveries-for-a-repository-webhook
        Delivery - an "event" that happened via webhook.

        Make a list of ids of each delivery in order to get all payload data via id in the future.

        :return: The list of the deliveries ids
        """
        webhook_id = self.get_webhook_id()
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/hooks/{webhook_id}/deliveries"
        list_deliveries_for_webhook = self._get_response(url)
        deliveries_ids = [delivery["id"] for delivery in list_deliveries_for_webhook]
        return deliveries_ids
    
    def _save_to_db(self, data):
        """
        Save the given data to the django model.

        :param data: Delivery payload
        :return: None
        """
        number = data["pull_request"]["number"]
        author = data["pull_request"]["user"]["login"]
        title = data["pull_request"]["title"]
        link = data["pull_request"]["url"]
        updated_at = data["pull_request"]["updated_at"]
        review_requested = ", ".join(
            [reviewer['login'] for reviewer in data["pull_request"]["requested_reviewers"]])

        obj, created = PullRequest.objects.update_or_create(
            number=number, link=link,
            defaults={"author": author, "title": title, "updated_at": updated_at, "review_requested": review_requested}
        )
    
    def load_webhook_data(self):
        """
        Retrieve payload from all deliveries via their ids
        https://docs.github.com/en/free-pro-team@latest/rest/webhooks/repo-deliveries?apiVersion=2022-11-28#get-a-delivery-for-a-repository-webhook

        Call a function to save the data we need to the db if type of the event is "review_requested"

        :return: None
        """
        deliveries_ids = self.get_deliveries_ids_list()
        webhook_id = self.get_webhook_id()
        for delivery_id in deliveries_ids:
            delivery = self._get_response(f"http://api.github.com/repos/"
                                          f"{self.owner}/{self.repo}/hooks/{webhook_id}/deliveries/{delivery_id}")
            if delivery["action"] == "review_requested":
                print('Received the {} event'.format(delivery["action"]))
                self._save_to_db(data=delivery["request"]["payload"])


class Command(BaseCommand):
    help = "Retrieves all PRs from the given repository"

    def handle(self, *args, **options):
        fetch_webhook_data = FetchWebhookData()
        fetch_webhook_data.load_webhook_data()
