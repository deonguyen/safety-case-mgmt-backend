import os
import tempfile

from django.db.models import Q

from sq_spec_portal_backend_spec.apps import SqSpecPortalBackendSpecConfig
from sq_spec_portal_backend_core.models.project_model import ProjectModel
from sq_spec_portal_backend_core.models.project_specification_model import (
    ProjectSpecificationModel,
)
from sq_spec_portal_backend_core.models.component_model import ComponentModel
from sq_spec_portal_backend_core.models.specification_model import SpecificationModel
from sq_spec_portal_backend_core.models.specification_revision_model import (
    SpecificationRevisionModel,
)
from sq_spec_portal_backend_core.models.code_implementation_trace_model import (
    CodeImplementationTraceModel,
)
from sq_spec_portal_backend_core.models.code_implementation_trace_log_model import (
    CodeImplementationTraceLogModel,
)
from sq_spec_portal_backend_spec.services import github_app_service
from sq_spec_portal_backend_spec.views.vertex_ai_view import VertexAIViewSet
from sq_spec_portal_backend_spec.services.specification_service import (
    parse_specification_content,
)
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import base64
import json
import re
import requests
import markdown
from bs4 import BeautifulSoup


def tree(branch, github_token, owner, project, repo, user, version):
    """
    Fetch the recursive tree structure of a GitHub repository.
    Expects 'owner', 'repo', and optionally 'branch' (default: main) in query params.
    """
    if not github_token:
        return Response(
            {"error": "Server configuration error: GITHUB_TOKEN not found."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not owner or not repo:
        return Response(
            {"error": "Parameters 'owner' and 'repo' are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # GitHub API to get the tree recursively
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return Response(
                {"error": "Repository or branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        response.raise_for_status()
        return Response(response.json(), status=status.HTTP_200_OK)
    except requests.RequestException as e:
        return Response(
            {"error": f"GitHub API call failed: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )


def last_two_commits(branch, github_token, owner, project, repo, user, version):
    """
    Fetch the last two commits of a branch from a GitHub repository.
    Expects an optional 'branch' in query params, otherwise defaults to server config.
    """
    if not github_token:
        return Response(
            {"error": "Server configuration error: GITHUB_TOKEN not found."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not owner or not repo:
        return Response(
            {"error": "Server configuration for GitHub owner and repo is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {"sha": branch, "per_page": 2}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return Response(
                {"error": "Repository or branch not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        response.raise_for_status()
        return Response(response.json(), status=status.HTTP_200_OK)
    except requests.RequestException as e:
        return Response(
            {"error": f"GitHub API call failed: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )


def get_file_content_base64(
    branch,
    github_token,
    owner,
    path,
    project,
    ref,
    repo,
    user,
    version,
):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {github_token}"}
    params = {"ref": ref}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        response_json = response.json()
        content_b64 = (
            response_json.get("content") if isinstance(response_json, dict) else None
        )
        return content_b64
    except requests.RequestException:
        return None
    return None


def search_text_recursive(github_token, owner, repo, path, ref, search_prefix):
    """
    Helper method to recursively fetch all files and search their content for a prefix.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": ref}
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 404:
        return []

    response.raise_for_status()
    items = response.json()

    if not isinstance(items, list):
        items = [items]

    results = []
    # Matches word boundary followed by the target prefix and any subsequent word characters
    pattern = re.compile(rf"\b{re.escape(search_prefix)}\w*", re.IGNORECASE)

    for item in items:
        if item.get("type") == "file":
            download_url = item.get("download_url")
            if download_url:
                content_resp = requests.get(download_url, headers=headers)
                if content_resp.status_code == 200:
                    try:
                        # Decode as UTF-8 to safely ignore binary files
                        text_content = content_resp.content.decode("utf-8")
                        matches = list(set(pattern.findall(text_content)))
                        if matches:
                            print("Add item: " + item)
                            results.append(
                                {
                                    "name": item.get("name"),
                                    "path": item.get("path"),
                                    "sha": item.get("sha"),
                                    "url": item.get("url"),
                                    "html_url": item.get("html_url"),
                                    "git_url": item.get("git_url"),
                                    "download_url": item.get("download_url"),
                                    "matches": matches,
                                }
                            )
                    except UnicodeDecodeError:
                        # Skip binary or non-UTF8 files
                        pass
        elif item.get("type") == "dir":
            results.extend(
                search_text_recursive(
                    github_token, owner, repo, item.get("path"), ref, search_prefix
                )
            )

    return results


def get_releases(github_token, owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    releases = []
    page = 1

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        # Stop looping if there are no more results
        data = response.json()
        if not data:
            break

        # for release in data:
        #     print(f"Release Name: {release.get('name')}")
        #     print(f"Tag Version:  {release.get('tag_name')}")
        #     print(f"Published At: {release.get('published_at')}")
        #     # print("-" * 40)
        #     print("Downloading asset ZIP file")
        #     # Download ZIP file asset of release
        #     zipball_response = requests.get(release.get('zipball_url'), headers=headers, stream=True)
        #     zipball_response.raise_for_status()

        #     # Save the zip file
        #     with open(f"{release.get('tag_name')}.zip", "wb") as file:
        #         for chunk in zipball_response.iter_content(chunk_size=8192):
        #             file.write(chunk)

        #     print("Download complete!")
        #     print("-" * 40)
        releases.extend(data)
        page += 1

    return releases


def get_release_by_tag(github_token, owner, repo, release_tag):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{release_tag}"

    # Optional: Add headers for authentication if the repo is private
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        print(f"Release Name: {release_data['name']}")
        print(f"HTML URL: {release_data['html_url']}")
        return release_data
    else:
        print(f"Failed to fetch release: {response.status_code}")
        print(response.json())
        return None


def download_release_zipfile(github_token, zipball_url, temp_dir, tag_name):
    try:
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        zipball_response = requests.get(zipball_url, headers=headers, stream=True)
        zipball_response.raise_for_status()

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        temp_file = tempfile.mkdtemp(dir=temp_dir)
        file_path = os.path.join(temp_file, f"{tag_name}.zip")

        # Save the zip file
        with open(file_path, "wb") as file:
            for chunk in zipball_response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException:
        return None
    return Response(
        {
            "message": f"Downloaded file: {file_path}",
            "file_path": file_path,
        },
        status=status.HTTP_200_OK,
    )


def search_prefix_in_repos(github_token, owner, repo, search_prefix):
    REPO = repo
    TOKEN = github_token
    PREFIX_QUERY = search_prefix  # or exact term / prefix

    url = f"https://github.com{search_prefix}+repo:{owner}/{repo}"
    # url = "https://api.github.com/search/code"
    query = f"{PREFIX_QUERY} repo:{REPO}"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    params = {
        "q": query,
    }

    # response = requests.get(url, headers=headers, params=params)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Total matches: {data.get('total_count')}")
        for item in data.get("items", []):
            print(f"File: {item['path']} | URL: {item['html_url']}")
    else:
        print(f"Error {response.status_code}: {response.json()}")


def search_keyword_in_repos_code(github_token, keyword, owner, repo):
    """
    Searches for code on GitHub using the legacy REST API endpoint.
    """
    url = "https://api.github.com/search/code"

    # 1. Build the query string with qualifiers
    query_parts = [keyword]
    if repo:
        query_parts.append(f"repo:{owner}/{repo}")

    query_string = " ".join(query_parts)

    # 2. Set up headers (Authentication & API Version)
    # GitHub strongly recommends providing an explicit API version header
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    params = {
        "q": query_string,
        "per_page": 5,  # Max 100 per page
    }

    # 3. Execute request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def search_keyword_in_repos_issues_and_pullrequests(github_token, keyword, owner, repo):
    """
    Searches for code on GitHub using the legacy REST API endpoint.
    """
    url = "https://api.github.com/search/issues"

    # 1. Build the query string with qualifiers
    query_parts = [keyword]
    if repo:
        query_parts.append(f"repo:{owner}/{repo}")

    query_string = " ".join(query_parts)

    # 2. Set up headers (Authentication & API Version)
    # GitHub strongly recommends providing an explicit API version header
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    params = {
        "q": query_string,
        "per_page": 5,  # Max 100 per page
    }

    # 3. Execute request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def process_import_traceability_for_repos(project, github_url, user):
    github_token = github_app_service.get_github_app_installation_token(
        int(os.environ.get("GITHUB_APP_ID")),
        int(os.environ.get("GITHUB_APP_TMCAUTONOMY_INSTALLATION_ID")),
    )
    if not github_token:
        return Response(
            {"error": "Server configuration error: GitHub token not available."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    owner = None
    repo = None
    url_to_parse = github_url
    # Extract GitHub owner, repo, and branch if a full GitHub URL is provided
    if url_to_parse and "github.com" in url_to_parse:
        match = re.search(
            r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?", url_to_parse
        )
        if match:
            owner = match.group(1)
            repo = match.group(2).replace(".git", "")

    specifications = SpecificationModel.objects.filter(
        project=project,
        source="Github",
        type__in=["Specification", "Sub Specification"],
    )
    for spec in specifications:
        try:
            search_code_result = search_keyword_in_repos_code(
                github_token=github_token, keyword=spec.code, owner=owner, repo=repo
            )
            if int(search_code_result.get("total_count")) > 0:
                print("Found code implement: " + spec.code)
                project_spec = ProjectSpecificationModel.objects.filter(
                    project=project, specification=spec
                ).first()
                latest_revision = (
                    SpecificationRevisionModel.objects.filter(
                        specification_id=project_spec.specification_id
                    )
                    .order_by("-change_date")
                    .first()
                )
                trace, _ = CodeImplementationTraceModel.objects.update_or_create(
                    project=project,
                    project_specification=project_spec,
                    specification=project_spec.specification,
                    type="Code",
                    defaults={
                        "specification_revision": latest_revision,
                        "code_implementation_status": f"draft_{project_spec.id}",
                    },
                )
                for item in search_code_result.get("items"):
                    trace_log, _ = (
                        CodeImplementationTraceLogModel.objects.update_or_create(
                            project=project,
                            code_implementation_trace=trace,
                            path=item.get("path"),
                            name=item.get("name"),
                            defaults={
                                "sha": item.get("sha"),
                                "html_url": item.get("html_url"),
                            },
                        )
                    )
            else:
                print("Not found: " + spec.code)

            search_pr_result = search_keyword_in_repos_issues_and_pullrequests(
                github_token=github_token, keyword=spec.code, owner=owner, repo=repo
            )
            if int(search_pr_result.get("total_count")) > 0:
                print("Found pull reuqest implement: " + spec.code)
                project_spec = ProjectSpecificationModel.objects.filter(
                    project=project, specification=spec
                ).first()
                latest_revision = (
                    SpecificationRevisionModel.objects.filter(
                        specification_id=project_spec.specification_id
                    )
                    .order_by("-change_date")
                    .first()
                )
                trace, _ = CodeImplementationTraceModel.objects.update_or_create(
                    project=project,
                    project_specification=project_spec,
                    specification=project_spec.specification,
                    type="Pull request",
                    defaults={
                        "specification_revision": latest_revision,
                        "code_implementation_status": f"draft_{project_spec.id}",
                    },
                )
                for item in search_pr_result.get("items"):
                    trace_log, _ = (
                        CodeImplementationTraceLogModel.objects.update_or_create(
                            project=project,
                            code_implementation_trace=trace,
                            path=item.get("node_id"),
                            name=item.get("number"),
                            defaults={
                                "sha": item.get("sha"),
                                "html_url": item.get("html_url"),
                                "pull_request_comments": item.get("body"),
                                "pull_request_title": item.get("title"),
                            },
                        )
                    )
            else:
                print("Not found pull reuqest implement: " + spec.code)
        except Exception as e:
            return Response(
                {"message": f"Error sync traceability: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    print("Success full sync specification implementation")
    return Response(
        {"message": "Sync successful"},
        status=status.HTTP_200_OK,
    )

def process_import_traceability_from_repos_code_search(project, github_url, user):
    github_token = github_app_service.get_github_app_installation_token(
        int(os.environ.get("GITHUB_APP_ID")),
        int(os.environ.get("GITHUB_APP_TMCAUTONOMY_INSTALLATION_ID")),
    )
    if not github_token:
        return Response(
            {"error": "Server configuration error: GitHub token not available."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    owner = None
    repo = None
    url_to_parse = github_url
    # Extract GitHub owner, repo, and branch if a full GitHub URL is provided
    if url_to_parse and "github.com" in url_to_parse:
        match = re.search(
            r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?", url_to_parse
        )
        if match:
            owner = match.group(1)
            repo = match.group(2).replace(".git", "")

    specifications = SpecificationModel.objects.filter(
        project=project,
        source="Github",
        type__in=["Specification", "Sub Specification"],
    )
    for spec in specifications:
        try:
            search_code_result = search_keyword_in_repos_code(
                github_token=github_token, keyword=spec.code, owner=owner, repo=repo
            )
            if int(search_code_result.get("total_count")) > 0:
                print("Found code implement: " + spec.code)
                project_spec = ProjectSpecificationModel.objects.filter(
                    project=project, specification=spec
                ).first()
                latest_revision = (
                    SpecificationRevisionModel.objects.filter(
                        specification_id=project_spec.specification_id
                    )
                    .order_by("-change_date")
                    .first()
                )
                trace, _ = CodeImplementationTraceModel.objects.update_or_create(
                    project=project,
                    project_specification=project_spec,
                    specification=project_spec.specification,
                    type="Code",
                    defaults={
                        "specification_revision": latest_revision,
                        "code_implementation_status": f"draft_{project_spec.id}",
                    },
                )
                for item in search_code_result.get("items"):
                    trace_log, _ = (
                        CodeImplementationTraceLogModel.objects.update_or_create(
                            project=project,
                            code_implementation_trace=trace,
                            path=item.get("path"),
                            name=item.get("name"),
                            defaults={
                                "sha": item.get("sha"),
                                "html_url": item.get("html_url"),
                            },
                        )
                    )
            else:
                print("Not found code implement: " + spec.code)
        except Exception as e:
            return Response(
                {"message": f"Error sync traceability: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    print("Success full sync specification implementation")
    return Response(
        {"message": "Sync successful"},
        status=status.HTTP_200_OK,
    )

def process_import_traceability_from_repos_pr_search(project, github_url, user):
    github_token = github_app_service.get_github_app_installation_token(
        int(os.environ.get("GITHUB_APP_ID")),
        int(os.environ.get("GITHUB_APP_TMCAUTONOMY_INSTALLATION_ID")),
    )
    if not github_token:
        return Response(
            {"error": "Server configuration error: GitHub token not available."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    owner = None
    repo = None
    url_to_parse = github_url
    # Extract GitHub owner, repo, and branch if a full GitHub URL is provided
    if url_to_parse and "github.com" in url_to_parse:
        match = re.search(
            r"github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+))?", url_to_parse
        )
        if match:
            owner = match.group(1)
            repo = match.group(2).replace(".git", "")

    specifications = SpecificationModel.objects.filter(
        project=project,
        source="Github",
        type__in=["Specification", "Sub Specification"],
    )
    for spec in specifications:
        try:
            search_pr_result = search_keyword_in_repos_issues_and_pullrequests(
                github_token=github_token, keyword=spec.code, owner=owner, repo=repo
            )
            if int(search_pr_result.get("total_count")) > 0:
                print("Found pull reuqest implement: " + spec.code)
                project_spec = ProjectSpecificationModel.objects.filter(
                    project=project, specification=spec
                ).first()
                latest_revision = (
                    SpecificationRevisionModel.objects.filter(
                        specification_id=project_spec.specification_id
                    )
                    .order_by("-change_date")
                    .first()
                )
                trace, _ = CodeImplementationTraceModel.objects.update_or_create(
                    project=project,
                    project_specification=project_spec,
                    specification=project_spec.specification,
                    type="Pull request",
                    defaults={
                        "specification_revision": latest_revision,
                        "code_implementation_status": f"draft_{project_spec.id}",
                    },
                )
                for item in search_pr_result.get("items"):
                    trace_log, _ = (
                        CodeImplementationTraceLogModel.objects.update_or_create(
                            project=project,
                            code_implementation_trace=trace,
                            path=item.get("node_id"),
                            name=item.get("number"),
                            defaults={
                                "sha": item.get("sha"),
                                "html_url": item.get("html_url"),
                            },
                        )
                    )
            else:
                print("Not found pull reuqest implement: " + spec.code)
        except Exception as e:
            return Response(
                {"message": f"Error sync traceability: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    print("Success full sync specification implementation")
    return Response(
        {"message": "Sync successful"},
        status=status.HTTP_200_OK,
    )