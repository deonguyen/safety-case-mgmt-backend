import os
import google.auth
from sq_spec_portal_backend_spec.apps import SqSpecPortalBackendSpecConfig
from google.oauth2 import service_account


def get_gcp_credential():
    try:
        credentials = None
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        google_creds_path = os.path.realpath(os.environ.get("GOOGLE_CREDENTIALS_FILE"))
        if google_creds_path and os.path.exists(google_creds_path):
            credentials = service_account.Credentials.from_service_account_file(
                google_creds_path,
                scopes=scopes,
            )
        return credentials
    except Exception as e:
        print(f"Failed to retrieve service account credentials: {e}")
        return None