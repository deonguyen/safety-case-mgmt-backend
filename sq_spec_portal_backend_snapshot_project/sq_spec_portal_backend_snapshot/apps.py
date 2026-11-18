import os

from django.apps import AppConfig


class SqSpecPortalBackendSnapshotConfig(AppConfig):
    name = "sq_spec_portal_backend_snapshot"

    WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
