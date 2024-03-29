from django.core.management.base import BaseCommand, CommandError
import requests
from utils.common_functions import save_webhook_payload
from django.conf import settings


class FetchWebhookData:
    token = settings.GITHUB_TOKEN
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
        try:
            webhook_id = list_repository_webhooks[0]["id"]
            return webhook_id
        except KeyError as e:
            print(f'KeyError: {e}. Probably there is no payload data - "Bad credentials" error has occurred.')
            return

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
                save_webhook_payload(delivery["request"]["payload"])


class Command(BaseCommand):
    help = "Retrieves all PRs from the given repository"

    def handle(self, *args, **options):
        try:
            fetch_webhook_data = FetchWebhookData()
            fetch_webhook_data.load_webhook_data()
        except Exception as e:
            print(f"An exception occurred: {e}")
            return
