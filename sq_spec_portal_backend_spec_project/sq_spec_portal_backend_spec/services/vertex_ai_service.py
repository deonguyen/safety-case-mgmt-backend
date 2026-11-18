
from sq_spec_portal_backend_spec.apps import SqSpecPortalBackendSpecConfig
from vertexai.generative_models import GenerativeModel
import vertexai

from sq_spec_portal_backend_spec.services.google_cloud_service import get_gcp_credential


def compare_diff_summary(content1, content2):
    """
    Uses Google Vertex AI to generate a summary of differences between two contents.
    """
    # Note: Ensure you have authenticated with Google Cloud CLI (`gcloud auth application-default login`)
    # and have set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION in your Django settings.
    try:
        # Use Application Default Credentials. This works for local dev (gcloud auth),
        # GKE (Workload Identity), and Cloud Run (attached service account).
        credentials = get_gcp_credential()
        # This will use the default credentials from the environment when running in Google Cloud
        vertexai.init(
            project=SqSpecPortalBackendSpecConfig.GOOGLE_PROJECT_ID,
            location=SqSpecPortalBackendSpecConfig.GOOGLE_LOCATION,
            credentials=credentials,
        )
        model = GenerativeModel("gemini-1.5-pro-001")

        prompt = f"""
            You are an expert software engineer. Your task is to summarize the changes between two versions of a content.
            Provide a concise, human-readable summary. Focus on the semantic meaning of the changes.
            
            Here is the new version of the content:
            ---NEW VERSION---
            {content1}
            ---END NEW VERSION---

            Here is the old version of the content:
            ---OLD VERSION---
            {content2}
            ---END OLD VERSION---
           
            Summary of changes:
            """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate summary due to an error: {e}"


def generate_diagram(input_data, output_data):
    """
    Uses Google Vertex AI to generate a diagram (Mermaid JS format) based on input and output descriptions.
    """
    try:
        credentials = get_gcp_credential()
        vertexai.init(
            project=SqSpecPortalBackendSpecConfig.GOOGLE_PROJECT_ID,
            location=SqSpecPortalBackendSpecConfig.GOOGLE_LOCATION,
            credentials=credentials,
        )

        # Using a more recent and capable model for diagram generation
        model = GenerativeModel("gemini-1.5-flash-001")

        prompt = f"""
            You are an expert software architect. Your task is to generate a diagram in the Mermaid JS format 
            based on the provided input and output descriptions.
            
            Input description:
            {input_data}
            
            Output description:
            {output_data}
            
            Provide ONLY the valid Mermaid JS code block (e.g., starting with ```mermaid and ending with ```).
            Do not include any other explanations or surrounding text.
            """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate diagram due to an error: {e}"
