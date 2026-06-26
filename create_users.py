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

    # PASO 1 — Crear usuario (user_name = email, requerido por la API)
    payload = {
        "user_name":     user["email"],
        "email_address": user["email"],
        "first_name":    user["first_name"],
        "last_name":     user["last_name"],
        "active":        True,
        "userType":      "VOSP",
        "pin_required":  True
    }

    r_create = requests.post(
        BASE_URL,
        auth=auth,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    print("-------------------------------------")
    print(f"Creando: {user['email']}")
    print(f"Status:  {r_create.status_code}")

    if r_create.status_code not in (200, 201):
        print(f"ERROR al crear: {r_create.text}")
        continue

    created = r_create.json()
    user_id = created.get("user_id")

    if not user_id:
        print(f"ERROR: sin user_id. Respuesta: {created}")
        continue

    print(f"user_id: {user_id}")

    # PASO 2 — Sobreescribir username con el valor del JSON
    r_put = requests.put(
        f"{BASE_URL}/{user_id}?partial=true",
        auth=auth,
        headers=HEADERS,
        data=json.dumps({"user_name": user["username"]})
    )

    print(f"PUT username → Status: {r_put.status_code}")
    print(f"PUT response body: {r_put.text}")

    if r_put.status_code not in (200, 204):
        print(f"ERROR en PUT: {r_put.text}")
    else:
        print(f"Username '{user['username']}' asignado.")
