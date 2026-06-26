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

results = []

for user in users:

    print("=============================================")
    print(f"[INICIO] Procesando usuario: {user['email']}")
    print(f"[REQUEST POST] URL: {BASE_URL}")

    payload = {
        "user_name":     user["email"],
        "email_address": user["email"],
        "first_name":    user["first_name"],
        "last_name":     user["last_name"],
        "active":        True,
        "userType":      "VOSP",
        "pin_required":  True
    }

    print(f"[REQUEST POST] Payload enviado:")
    print(json.dumps(payload, indent=2))

    r_create = requests.post(
        BASE_URL,
        auth=auth,
        headers=HEADERS,
        data=json.dumps(payload)
    )

    print(f"[RESPONSE POST] Status: {r_create.status_code}")
    print(f"[RESPONSE POST] Body:")
    print(json.dumps(r_create.json(), indent=2) if r_create.headers.get("Content-Type","").startswith("application/json") else r_create.text)

    if r_create.status_code not in (200, 201):
        print(f"[ERROR] Fallo en creacion. Se omite el PUT.")
        results.append({
            "email": user["email"],
            "username_solicitado": user["username"],
            "status_post": r_create.status_code,
            "error_post": r_create.text,
            "user_id": None,
            "username_asignado_post": None,
            "status_put": None,
            "username_asignado_put": None
        })
        continue

    created = r_create.json()
    user_id = created.get("user_id")
    username_post = created.get("user_name")

    print(f"[INFO] user_id obtenido: {user_id}")
    print(f"[INFO] user_name asignado por Veracode en POST: {username_post}")

    # PASO 2 — Intentar cambiar username via PUT
    put_payload = {"user_name": user["username"]}

    print(f"[REQUEST PUT] URL: {BASE_URL}/{user_id}?partial=true")
    print(f"[REQUEST PUT] Payload enviado:")
    print(json.dumps(put_payload, indent=2))

    r_put = requests.put(
        f"{BASE_URL}/{user_id}?partial=true",
        auth=auth,
        headers=HEADERS,
        data=json.dumps(put_payload)
    )

    print(f"[RESPONSE PUT] Status: {r_put.status_code}")
    print(f"[RESPONSE PUT] Body:")
    print(json.dumps(r_put.json(), indent=2) if r_put.headers.get("Content-Type","").startswith("application/json") else r_put.text)

    username_put = r_put.json().get("user_name") if r_put.status_code in (200, 204) else None

    print(f"[INFO] user_name asignado por Veracode en PUT: {username_put}")

    if username_put == user["username"]:
        print(f"[OK] Username '{user['username']}' asignado correctamente.")
    else:
        print(f"[DISCREPANCIA] Se solicitó username '{user['username']}' pero Veracode asignó '{username_put}'")

    results.append({
        "email":                  user["email"],
        "username_solicitado":    user["username"],
        "status_post":            r_create.status_code,
        "username_asignado_post": username_post,
        "user_id":                user_id,
        "status_put":             r_put.status_code,
        "username_asignado_put":  username_put
    })

# Resumen final
print("")
print("=============================================")
print("RESUMEN FINAL")
print("=============================================")
for r in results:
    print(f"Email            : {r['email']}")
    print(f"Username pedido  : {r['username_solicitado']}")
    print(f"Username POST    : {r['username_asignado_post']}")
    print(f"Username PUT     : {r['username_asignado_put']}")
    print(f"Coincide         : {'SI' if r['username_asignado_put'] == r['username_solicitado'] else 'NO — Veracode ignoro el cambio'}")
    print("---------------------------------------------")

# Exportar evidencia a JSON
with open("evidencia_veracode.json", "w") as f:
    json.dump(results, f, indent=2)

print("")
print("[INFO] Evidencia exportada a evidencia_veracode.json")
