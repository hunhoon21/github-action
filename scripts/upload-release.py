import os
import requests
from pathlib import Path
import hashlib

print("say hello")

TAG = os.environ["GITHUB_REF_NAME"]

REPO = os.environ["GITHUB_REPOSITORY"]

is_develop = True if "dev" in TAG.split("-") else False

BASE_URL = os.environ["base_dev_admin"] if is_develop else os.environ["base_admin"]

auth_url = f"{BASE_URL}/admin_user/authenticate"

# get auth headers to call Link License API
email = "admin@test.com"
pw = "12345aA!"
body = {"email": email, "password": pw}

resp = requests.post(auth_url, json=body)
token = resp.json()["result"]

auth_token = f"Bearer {token['bearer_token']}"
headers = {"Authorization": auth_token}

# Check if this release exists
link_release_get_url = f"{BASE_URL}/link_release/get"
body = {
    "link_ver": TAG.split("-")[0]
}
resp = requests.post(link_release_get_url, headers=headers, json=body)
print(resp.json())
print()
link_release_result = None
if resp.json()["ok"]:
    link_release_result = resp.json()["result"]["link_release"]


url = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
resp = requests.get(url)
print(resp.json())
release_on_github = resp.json()

link_release_create_url = f"{BASE_URL}/link_release/create"
link_release_update_url = f"{BASE_URL}/link_release/update"

commit_url = f"https://api.github.com/repos/{REPO}/commits/{TAG}"
resp = requests.get(commit_url)
commit_id = resp.json()["sha"]
link_ver = TAG.split("-")[0]

if link_release_result is None:
    body = {
        "link_ver": link_ver,
        "link_ver_name": TAG,
        "link_ver_major": int(link_ver.split(".")[0]),
        "link_ver_minor": int(link_ver.split(".")[1]),
        "link_ver_micro": int(link_ver.split(".")[2]),
        "commit_id": commit_id,
        "description": release_on_github["body"],
        "release_note": release_on_github["body"],
        "release_date": release_on_github["created_at"],
    }
    resp = requests.post(link_release_create_url, headers=headers, json=body)
    link_release_id = resp.json()["result"]["link_release_id"]
else:
    body = {
        "id": link_release_result["id"],
        "link_ver": link_ver,
        "link_ver_name": TAG,
        "link_ver_major": int(link_ver.split(".")[0]),
        "link_ver_minor": int(link_ver.split(".")[1]),
        "link_ver_micro": int(link_ver.split(".")[2]),
        "commit_id": commit_id,
        "description": release_on_github["body"],
        "release_note": release_on_github["body"],
        "release_date": release_on_github["created_at"],
        "state": link_release_result["state"]
    }
    resp = requests.post(link_release_update_url, headers=headers, json=body)
    link_release_id = resp.json()["result"]["link_release_id"]

link_release_file_get_url = f"{BASE_URL}/link_release_file/get_by_info"
link_release_file_create_url = f"{BASE_URL}/link_release_file/create"
link_release_file_update_url = f"{BASE_URL}/link_release_file/update"

if "assets" in release_on_github:
    assets = release_on_github["assets"]

    for asset in assets:
        asset_url = asset["url"]
        asset_name = asset["name"]
        asset_size = asset["size"]
        asset_date = asset["updated_at"]

        if Path(asset_name).suffix not in [".whl"]:
            continue

        py_ver = ""
        os = ""
        arch = ""
        product_type = "whl"

        splitted_link_ver = asset_name.split("-")[1].split(".") 
        link_ver = f"{splitted_link_ver[0]}.{splitted_link_ver[1]}.{splitted_link_ver[2]}"

        if "cp36" in asset_name:
            py_ver = "3.6"
        elif "cp37" in asset_name:
            py_ver = "3.7"
        elif "cp38" in asset_name:
            py_ver = "3.8"
        elif "cp39" in asset_name:
            py_ver = "3.9"
        
        if "linux" in asset_name:
            os = "linux"
        elif "win" in asset_name:
            os = "windows"
        elif "macosx" in asset_name:
            os = "mac"
        
        if "arm64" in asset_name:
            arch = "arm64"
        else:
            arch = "x86_64"
        
        body = {
            "link_ver": link_ver,
            "py_ver": py_ver,
            "os": os,
            "arch": arch,
            "product_type": product_type,
        }

        resp = requests.post(link_release_file_get_url, headers=headers, json=body)

        link_release_file_result = None
        if resp.json()["ok"]:
            link_release_file_result = resp.json()["result"]["link_release_file"]
        
        headers = {
            "Accept": "application/octet-stream"
        }
        resp = requests.get(asset_url, headers=headers)
        content = resp.content

        md5 =hashlib.md5(content).hexdigest()
        if link_release_file_result is None:
            body = {
                "link_release_id": link_release_id,
                "link_ver": link_ver,
                "link_ver_name": TAG,
                "link_ver_major": int(link_ver.split(".")[0]),
                "link_ver_minor": int(link_ver.split(".")[1]),
                "link_ver_micro": int(link_ver.split(".")[2]),
                "commit_id": commit_id,
                "release_date": asset_date,
                "py_ver": py_ver,
                "os": os,
                "arch": arch,
                "product_type": product_type,
                "size": len(content),
                "md5": md5,
                "filename": asset_name,
                "s3_bucket": "string",
                "s3_path": "string",
            }
            resp = requests.post(link_release_file_create_url, headers=headers, json=body)

