import secrets

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates a new secret key for GitHub webhooks."

    def handle(self, *args, **options):
        secret = secrets.token_hex(32)
        self.stdout.write(f"Generated GitHub webhook secret: {secret}")
        self.stdout.write(
            "Please add this to your environment variables as GITHUB_WEBHOOK_SECRET."
        )