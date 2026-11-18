from py_jama_rest_client.client import JamaClient
import json
import os
import time


def get_items_by_project(client, project_id):
    # Alternatively, for Basic authentication:
    # client = JamaClient("https://yourdomain.jamacloud.com", credentials=("username", "password"))

    # 2. Define the project ID you want to fetch items from
    # project_id = 368

    # 3. Fetch all items (the SDK automatically handles pagination internally)
    items = client.get_items(project_id)

    # 4. Print or process your items
    output_file = "up_down_stream_result.json"

    existing = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            existing = json.load(f)

    for item in items:
        # print(f"ID: {item.get('id')} | Name: {item.get('fields', {}).get('name')}")
        # existing.append(item)
        items_upstream_relationships = client.get_items_upstream_relationships(
            item.get("id")
        )
        for up in items_upstream_relationships:
            existing.append(up)
            time.sleep(5)
        items_downstream_relationships = client.get_items_downstream_relationships(
            item.get("id")
        )
        for down in items_downstream_relationships:
            existing.append(down)
            time.sleep(5)

    with open(output_file, "w") as f:
        json.dump(existing, f, indent=2)


def get_items_version(client, item_id):
    # Alternatively, for Basic authentication:
    # client = JamaClient("https://yourdomain.jamacloud.com", credentials=("username", "password"))

    # 2. Set your target item ID
    # item_id = 12345

    # 3. Retrieve all versions of the item
    versions = client.get_item_versions(item_id)
    # 4. Print or process your items
    output_file = "version_result.json"

    existing = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            existing = json.load(f)

    for version in versions:
        print(f"Version Number: {version.get('versionNumber')}")
        print(f"Created By: {version.get('createdBy')}")
        print(f"Date Modified: {version.get('lastModifiedDate')}")
        print("-" * 20)
        existing.append(version)

    with open(output_file, "w") as f:
        json.dump(existing, f, indent=2)


def get_items_version(client, item_id):
    # Alternatively, for Basic authentication:
    # client = JamaClient("https://yourdomain.jamacloud.com", credentials=("username", "password"))

    # 2. Set your target item ID
    # item_id = 12345

    # 3. Retrieve all versions of the item
    versions = client.get_item_versions(item_id)
    # 4. Print or process your items
    output_file = "version_result.json"

    existing = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            existing = json.load(f)

    for version in versions:
        print(f"Version Number: {version.get('versionNumber')}")
        print(f"Created By: {version.get('createdBy')}")
        print(f"Date Modified: {version.get('lastModifiedDate')}")
        print("-" * 20)
        existing.append(version)

    with open(output_file, "w") as f:
        json.dump(existing, f, indent=2)


def get_relationship_types():
    # Alternatively, for Basic authentication:
    # client = JamaClient("https://yourdomain.jamacloud.com", credentials=("username", "password"))

    # 2. Define the project ID you want to fetch items from
    # project_id = 368

    # 3. Fetch all items (the SDK automatically handles pagination internally)
    items = client.get_relationship_types()

    # 4. Print or process your items
    output_file = "relationship_types_result.json"

    existing = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            existing = json.load(f)

    for item in items:
        print(f"item: {item}")
        existing.append(item)

    with open(output_file, "w") as f:
        json.dump(existing, f, indent=2)


# def get_relationship_types():
#     # Alternatively, for Basic authentication:
#     # client = JamaClient("https://yourdomain.jamacloud.com", credentials=("username", "password"))

#     # 2. Define the project ID you want to fetch items from
#     # project_id = 368

#     # 3. Fetch all items (the SDK automatically handles pagination internally)
#     items = client.get_relationship_types()

#     # 4. Print or process your items
#     output_file = "relationship_bata_by_type_result.json"

#     existing = []
#     if os.path.exists(output_file):
#         with open(output_file, "r") as f:
#             existing = json.load(f)

#     for item in items:
#         try:
#             relationship_items = client.get_relationship(item.get("id"))
#             for relationship_item in relationship_items:
#                 print(f"relationship item: {relationship_item}")
#                 existing.append(relationship_item)
#         except:
#             continue
#     with open(output_file, "w") as f:
#         json.dump(existing, f, indent=2)


def lazy_load_jama_items(client: JamaClient, jama_project_id: int, page_size: int = 20):
    """
    A generator that lazy-loads items from Jama page-by-page.
    Only queries the API when the next batch is needed.
    """
    start_index = 0

    while True:
        # Access the core HTTP client wrapper inside py-jama-rest-client
        # Endpoint documentation: GET /items
        resource_path = "items"
        params = {
            "project": jama_project_id,
            "startAt": start_index,
            "maxResults": page_size,
        }

        # client._JamaClient__core provides raw access to Jama's REST client
        response = client._JamaClient__core.get(resource_path, params=params)
        response.raise_for_status()

        data_page = response.json()
        items = data_page.get("data", [])

        # Break loop if no more items are returned
        if not items:
            break

        # Yield items one by one
        for item in items:
            yield item

        # Check meta information to see if we reached the end of results
        page_info = data_page.get("meta", {}).get("pageInfo", {})
        total_results = page_info.get("totalResults", 0)

        start_index += len(items)
        if start_index >= total_results:
            break

def get_jama_tem_types(client: JamaClient, jama_project_id: int):
    # 3. Retrieve all items in the project to extract their unique item types
    try:
        # Fetch all item types across the Jama instance
        item_types = client.get_item_types()

        # Print the retrieved item types
        # for item_type in item_types:
        #     print(f"ID: {item_type.get('id')}, Name: {item_type.get('display')}")
        return item_types
    except Exception as e:
        print(f"An error occurred: {e}")


# def main():
#     get_items_by_project(client, 368)

# if __name__ == "__main__":
#     main()


def jama_item_to_html(item_data: dict) -> str:
    """
    Converts a Jama API item dictionary into a structured HTML document.
    """
    # Extract core item properties safely
    item_id = item_data.get("id", "N/A")
    document_key = item_data.get("documentKey", "N/A")
    global_id = item_data.get("globalId", "N/A")

    # Extract fields dictionary
    fields = item_data.get("fields", {})
    item_name = fields.get("name", "Untitled Item")

    # Jama rich-text fields (like description) are already formatted as HTML strings
    item_description = fields.get("description", "<p>No description provided.</p>")

    # Build metadata rows from remaining fields
    metadata_rows = ""
    excluded_fields = {"name", "description"}
    for key, value in fields.items():
        if key not in excluded_fields:
            # Handle dictionary values (like picklist options) gracefully
            if isinstance(value, dict):
                value_str = value.get("name", json.dumps(value))
            else:
                value_str = str(value)

            metadata_rows += f"<tr><th>{key}</th><td>{value_str}</td></tr>\n"

    # Generate the full HTML structure
    html_template = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{documentKey}: {item_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
            .header {{ border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }}
            .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            .meta-table th, .meta-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .meta-table th {{ background-color: #f2f2f2; width: 25%; }}
            .description {{ background: #fafafa; border-left: 4px solid #0056b3; padding: 15px; border-radius: 4px; }}
            .section-title {{ color: #0056b3; margin-top: 30px; }}
        </style>
    </head>
    <body>

        <div class="header">
            <h1>[{document_key}] {item_name}</h1>
            <p><strong>System ID:</strong> {item_id} | <strong>Global ID:</strong> {global_id}</p>
        </div>

        <h2 class="section-title">Item Fields</h2>
        <table class="meta-table">
            {metadata_rows}
        </table>

        <h2 class="section-title">Description</h2>
        <div class="description">
            {item_description}
        </div>

    </body>
    </html>
    """
    return html_template

def rule_base_parse_specification(raw_content):
    return ""