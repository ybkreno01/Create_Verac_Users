import json
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

URL = "https://api.veracode.com/api/authn/v2/users"

auth = RequestsAuthPluginVeracodeHMAC()

with open("users.json") as f:
    users = json.load(f)

for user in users:

    payload = {
        "user_name": user["username"],
        "email_address": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "active": True
    }

    r = requests.post(URL, auth=auth, json=payload)

    print("-------------------------------------")
    print(user["username"])
    print(r.status_code)
    print(r.text)
