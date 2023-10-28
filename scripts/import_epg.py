def write_to_github(content, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    # Try to fetch the SHA of the existing file
    try:
        response = requests.get(GITHUB_REPO_API, headers=headers)
        response.raise_for_status()
        sha = response.json().get('sha', '')
    except requests.RequestException as e:
        # If the file doesn't exist (404 error), create it
        if e.response.status_code == 404:
            print("File not found. Creating a new one...")
            sha = None
        else:
            print(f"Error fetching SHA for file: {e}")
            exit(1)

    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    data = {
        "message": "Updated merged EPG file",
        "content": encoded_content
    }

    if sha:  # If SHA is present, include it in the data (means we're updating the file)
        data["sha"] = sha

    try:
        response = requests.put(GITHUB_REPO_API, headers=headers, json=data)
        if response.status_code in [200, 201]:  # 200 for update, 201 for creation
            print("File successfully updated!")
        else:
            print(f"Failed to update. Status Code: {response.status_code}. Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error writing to GitHub: {e}")
        exit(1)
