import os
import boto3
from botocore.config import Config
from typing import Any, Dict, Optional, Tuple
import tempfile
import requests
from pathlib import Path
import hashlib


TAG = os.environ["GITHUB_REF_NAME"]
REPO = os.environ["GITHUB_REPOSITORY"]
print(f"{os.environ['GITHUB_SHA']=}")

# is_develop = True if "dev" in TAG.split("-") else False

# if is_develop:
#     BASE_URL = os.environ["DEV_ADMIN_BASE"]
#     ADMIN_EMAIL = os.environ["DEV_ADMIN_EMAIL"]
#     ADMIN_PW = os.environ["DEV_ADMIN_PW"]
#     AWS_ACCESS_KEY_ID = os.environ["DEV_AWS_ACCESS_KEY_ID"]
#     AWS_SECRET_ACCESS_KEY = os.environ["DEV_AWS_SECRET_ACCESS_KEY"]
#     S3_BUCKET = "mrx-link"
# else:
#     BASE_URL = os.environ["PROD_ADMIN_BASE"]
#     ADMIN_EMAIL = os.environ["PROD_ADMIN_EMAIL"]
#     ADMIN_PW = os.environ["PROD_ADMIN_PW"]
#     AWS_ACCESS_KEY_ID = os.environ["PROD_AWS_ACCESS_KEY_ID"]
#     AWS_SECRET_ACCESS_KEY = os.environ["PROD_AWS_SECRET_ACCESS_KEY"]
#     S3_BUCKET = "prod-mrx-link"


# def get_admin_headers(email: str, password: str):
#     auth_url = f"{BASE_URL}/admin_user/authenticate"

#     # get auth headers to call Link License API
#     body = {"email": email, "password": password}

#     resp = requests.post(auth_url, json=body)
#     token = resp.json()["result"]

#     auth_token = f"Bearer {token['bearer_token']}"
#     headers = {"Authorization": auth_token}
#     return headers


# def get_commit_id() -> str:
#     commit_url = f"https://api.github.com/repos/{REPO}/commits/{TAG}"
#     resp = requests.get(commit_url)
#     commit_id = resp.json()["sha"]
#     return commit_id


# def get_release_on_github() -> Dict[str, Any]:
#     url = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
#     resp = requests.get(url)
#     release_on_github = resp.json()
#     return release_on_github


# def get_link_release_info(admin_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
#     # Check if this release exists
#     link_release_get_url = f"{BASE_URL}/link_release/get"
#     body = {
#         "link_ver": TAG.split("-")[0]
#     }
#     resp = requests.post(link_release_get_url, admin_headers=admin_headers, json=body)
#     link_release_result = None
#     if resp.json()["ok"]:
#         link_release_result = resp.json()["result"]["link_release"]
    
#     return link_release_result

# def extract_asset_info_from_name(asset_name: str) -> Tuple(str):
#     py_ver = ""
#     os_type = ""
#     arch = ""
#     product_type = "whl"

#     if "cp36" in asset_name:
#         py_ver = "3.6"
#     elif "cp37" in asset_name:
#         py_ver = "3.7"
#     elif "cp38" in asset_name:
#         py_ver = "3.8"
#     elif "cp39" in asset_name:
#         py_ver = "3.9"
    
#     if "linux" in asset_name:
#         os_type = "linux"
#     elif "win" in asset_name:
#         os_type = "windows"
#     elif "macosx" in asset_name:
#         os_type = "mac"
    
#     if "arm64" in asset_name:
#         arch = "arm64"
#     else:
#         arch = "x86_64"
    
#     return py_ver, os_type, arch, product_type


# def get_release_file_info(admin_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
#     link_release_file_get_url = f"{BASE_URL}/link_release_file/get_by_info"
#     body = {
#         "link_ver": link_ver,
#         "py_ver": py_ver,
#         "os": os,
#         "arch": arch,
#         "product_type": product_type,
#     }

#     resp = requests.post(link_release_file_get_url, headers=admin_headers, json=body)

#     link_release_file_result = None
#     if resp.json()["ok"]:
#         link_release_file_result = resp.json()["result"]["link_release_file"]
#     return link_release_file_result


# def download_asset_content(asset_url: str) -> bytes:
#     headers = {
#         "Accept": "application/octet-stream"
#     }
#     resp = requests.get(asset_url, headers=headers)
#     asset_content = resp.content
#     return asset_content


# def upload_release_file_to_s3(
#     link_ver: str, py_ver: str, os_type: str, arch: str, release_file_name: str, release_file_content: bytes,
#     aws_access_key_id: str, aws_secret_access_key: str
# ):
#     s3_path = f"release/{link_ver}/{py_ver}/{os_type}/{arch}/{release_file_name}"
#     with tempfile.TemporaryDirectory() as tempdir:
#         temp_whl_path = os.path.join(tempdir, release_file_name)
        
#         with open(temp_whl_path, "wb") as f:
#             f.write(release_file_content)

#         cfg = Config(region_name="ap-northeast-2")
#         s3 = boto3.client(
#             "s3",
#             aws_access_key_id=aws_access_key_id,
#             aws_secret_access_key=aws_secret_access_key,
#             config=cfg
#         )
#         s3.upload_file(temp_whl_path, "mrx-link", s3_path)

#     return s3_path


# if __name__ == "__main__":
#     link_release_create_url = f"{BASE_URL}/link_release/create"
#     link_release_update_url = f"{BASE_URL}/link_release/update"
#     link_release_file_create_url = f"{BASE_URL}/link_release_file/create"
#     link_release_file_update_url = f"{BASE_URL}/link_release_file/update"

#     link_ver = TAG.split("-")[0]
#     commit_id = get_commit_id()

#     # Get ADMIN headers to authorize
#     admin_headers = get_admin_headers(email=ADMIN_EMAIL, password=ADMIN_PW)

#     # Get Link release information from Github Release
#     release_on_github = get_release_on_github()

#     # Get link release information from License Server
#     # It can be None if there is no link release
#     link_release_result = get_link_release_info(admin_headers=admin_headers)

#     if link_release_result is None:
#         # Create Link Release on the License Server
#         body = {
#             "link_ver": link_ver,
#             "link_ver_name": TAG,
#             "link_ver_major": int(link_ver.split(".")[0]),
#             "link_ver_minor": int(link_ver.split(".")[1]),
#             "link_ver_micro": int(link_ver.split(".")[2]),
#             "commit_id": commit_id,
#             "description": release_on_github["body"],
#             "release_note": release_on_github["body"],
#             "release_date": release_on_github["created_at"],
#         }
#         resp = requests.post(link_release_create_url, headers=admin_headers, json=body)
#         link_release_id = resp.json()["result"]["link_release_id"]
#     else:
#         # Update Link Release on the License Server
#         # Because Link Release already existed on the License Server
#         body = {
#             "id": link_release_result["id"],
#             "link_ver": link_ver,
#             "link_ver_name": TAG,
#             "link_ver_major": int(link_ver.split(".")[0]),
#             "link_ver_minor": int(link_ver.split(".")[1]),
#             "link_ver_micro": int(link_ver.split(".")[2]),
#             "commit_id": commit_id,
#             "description": release_on_github["body"],
#             "release_note": release_on_github["body"],
#             "release_date": release_on_github["created_at"],
#             "state": link_release_result["state"]
#         }
#         resp = requests.post(link_release_update_url, headers=admin_headers, json=body)
#         link_release_id = resp.json()["result"]["link_release_id"]


#     if "assets" in release_on_github:
#         assets = release_on_github["assets"]

#         for asset in assets:
#             asset_url = asset["url"]
#             asset_name = asset["name"]
#             asset_size = asset["size"]
#             asset_date = asset["updated_at"]

#             # Only handle whl file for now
#             if Path(asset_name).suffix not in [".whl"]:
#                 continue

#             splitted_link_ver = asset_name.split("-")[1].split(".") 
#             assert link_ver == f"{splitted_link_ver[0]}.{splitted_link_ver[1]}.{splitted_link_ver[2]}"

#             # Extract information from asset name
#             py_ver, os_type, arch, product_type = extract_asset_info_from_name(asset_name=asset_name)
            
#             link_release_file_result = get_release_file_info(admin_headers=admin_headers)
#             # Skip if both link release file on License Server & Github are same
#             if (
#                 link_release_file_result is not None
#                 and asset_name == link_release_file_result["filename"]
#                 and asset_size == link_release_file_result["size"]
#             ):
#                 continue
            
#             # Download whl content from release asset API
#             release_file_content = download_asset_content(asset_url=asset_url)
            
#             # Upload whl file to S3. It'll be link w/ License Server
#             s3_path = upload_release_file_to_s3(
#                 link_ver=link_ver,
#                 py_ver=py_ver,
#                 os_type=os_type,
#                 arch=arch,
#                 release_file_name=asset_name,
#                 release_file_content=release_file_content,
#                 aws_access_key_id=AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#             )
                
#             # hash release file as md5 to check file on the License Server
#             md5 = hashlib.md5(release_file_content).hexdigest()
#             if link_release_file_result is None:
#                 # Create Link Release File on the License Server
#                 body = {
#                     "link_release_id": link_release_id,
#                     "link_ver": link_ver,
#                     "link_ver_name": TAG,
#                     "link_ver_major": int(link_ver.split(".")[0]),
#                     "link_ver_minor": int(link_ver.split(".")[1]),
#                     "link_ver_micro": int(link_ver.split(".")[2]),
#                     "commit_id": commit_id,
#                     "release_date": asset_date,
#                     "py_ver": py_ver,
#                     "os": os,
#                     "arch": arch,
#                     "product_type": product_type,
#                     "size": len(release_file_content),
#                     "md5": md5,
#                     "filename": asset_name,
#                     "s3_bucket": S3_BUCKET,
#                     "s3_path": s3_path,
#                 }
#                 resp = requests.post(link_release_file_create_url, headers=admin_headers, json=body)
#                 assert resp.ok
            
#             else:
#                 # Update Link Release File on the License Server
#                 # Because Link Release File already existed on the License Server and It changed
#                 body = {
#                     "id": link_release_file_result["id"],
#                     "link_release_id": link_release_id,
#                     "link_ver": link_ver,
#                     "link_ver_name": TAG,
#                     "link_ver_major": int(link_ver.split(".")[0]),
#                     "link_ver_minor": int(link_ver.split(".")[1]),
#                     "link_ver_micro": int(link_ver.split(".")[2]),
#                     "commit_id": commit_id,
#                     "release_date": asset_date,
#                     "py_ver": py_ver,
#                     "os": os,
#                     "arch": arch,
#                     "product_type": product_type,
#                     "size": len(release_file_content),
#                     "md5": md5,
#                     "filename": asset_name,
#                     "s3_bucket": S3_BUCKET,
#                     "s3_path": s3_path,
#                     "state": link_release_file_result["state"],
#                 }
#                 resp = requests.post(link_release_file_update_url, headers=admin_headers, json=body)
#                 assert resp.ok
