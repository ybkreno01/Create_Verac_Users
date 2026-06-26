import json
import requests
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

BASE_URL = "https://api.veracode.com/api/authn/v2/users"

auth = RequestsAuthPluginVeracodeHMAC()

HEADERS = {
    "Content-Type": "application/json"
}

with open("users.json") as f:
    users = json.load(f)

for user in users:

    payload = {
        "user_name":     user["username"],
        "email_address": user["email"],
        "first_name":    user["first_name"],
        "last_name":     user["last_name"],
        "active":        True,
        "userType":      "VOSP",
        "pin_required":  True
    }

    r = requests.post(
        BASE_URL,
        auth=auth,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    print("-------------------------------------")
    print(f"Creando: {user['username']} / {user['email']}")
    print(f"Status:  {r.status_code}")
    print(r.text)
