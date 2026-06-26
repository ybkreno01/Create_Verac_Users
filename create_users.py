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

    # PASO 1 — Crear usuario
    payload = {
        "email_address": user["email"],
        "first_name":    user["first_name"],
        "last_name":     user["last_name"],
        "active":        True,
        "user_type":     "HUMAN"
    }

    r_create = requests.post(BASE_URL, auth=auth, headers=HEADERS, json=payload)

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

    print(f"user_id obtenido: {user_id}")

    # PASO 2 — Asignar username personalizado
    r_patch = requests.put(
        f"{BASE_URL}/{user_id}",
        auth=auth,
        headers=HEADERS,
        json={"user_name": user["username"]}
    )

    print(f"PATCH username → Status: {r_patch.status_code}")

    if r_patch.status_code not in (200, 204):
        print(f"ERROR en PATCH: {r_patch.text}")
    else:
        print(f"Username '{user['username']}' asignado.")
