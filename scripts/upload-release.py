import os
import requests

print("say hello")

tag = os.environ["GITHUB_REF_NAME"]

url = f"https://api.github.com/repos/hunhoon21/github-action/releases/tags/{tag}"

resp = requests.get(url)
print(resp)
print(resp.text)