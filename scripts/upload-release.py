import os
import requests

print("say hello")

tag = os.environ["GITHUB_REF_NAME"]

is_develop = True if "dev" in tag.split("-") else False

base_url = os.environ["base_dev_admin"] if is_develop else os.environ["base_admin"]

auth_url = f"{base_url}/admin_user/authenticate"

email = "admin@test.com"
pw = "12345aA!"
body = {"email": email, "password": pw}

resp = requests.post(auth_url, json=body)
token = resp.json()["result"]

auth_token = f"Bearer {token['bearer_token']}"
headers = {"Authorization": auth_token}

# Check if this release exists
link_release_get_url = f"{base_url}/link_release/get"
body = {
    "link_ver": tag.split("-")[0]
}
resp = requests.post(link_release_get_url, headers=headers, json=body)
link_release_id = None
if resp.json()["ok"]:
    link_release_id = resp.json()["result"]["link_release"]["id"]

url = f"https://api.github.com/repos/hunhoon21/github-action/releases/tags/{tag}"
resp = requests.get(url)
print(resp.json())
