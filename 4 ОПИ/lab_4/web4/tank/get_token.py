import subprocess
import requests
import json
import random

BASE_URL = "http://localhost:8080"
AUTH_ENDPOINT = f"{BASE_URL}/api/auth/login"

USERS = [
    {"username": "testuser_1", "password": "123"},
    {"username": "testuser_2", "password": "123"},
    {"username": "testuser_3", "password": "123"}
]

def make_ammo(method, uri, tag, body="", token=""):
    req = f"{method} {uri} HTTP/1.1\r\n"
    req += f"Host: host.docker.internal:8080\r\n"
    req += f"Authorization: Bearer {token}\r\n"
    req += "Connection: keep-alive\r\n"

    if body:
        body_bytes = body.encode('utf-8')
        req += f"Content-Type: application/json\r\n"
        req += f"Content-Length: {len(body_bytes)}\r\n"
        req += "\r\n"
        req_bytes = req.encode('utf-8') + body_bytes
    else:
        req += "\r\n"
        req_bytes = req.encode('utf-8')

    header = f"{len(req_bytes)} {tag}\n".encode('utf-8')

    return header + req_bytes + b"\n"

user_tokens = []

for user in USERS:
    try:
        response = requests.post(AUTH_ENDPOINT, json=user)
        response.raise_for_status()
        token = response.json().get("token")
        user_tokens.append(token)
        print(f"  [+] Авторизован: {user['username']}")
    except Exception as e:
        print(f"  [!] Ошибка авторизации {user['username']}: {e}")

if not user_tokens:
    print("Не удалось получить ни одного токена!")
    exit(1)

SHOTS_PER_USER = 100

with open("ammo.txt", "wb") as f:
    for i in range(SHOTS_PER_USER):
        for token in user_tokens:
            x = random.choice([-5, -4, -3, -2, -1, 0, 1, 2, 3])
            y = round(random.uniform(-3, 5), 4)

            f.write(make_ammo(
                method="GET",
                uri="/api/hits",
                tag=f"get_history",
                token=token
            ))

            payload = json.dumps({"x": x, "y": y, "r": 3})
            f.write(make_ammo(
                method="POST",
                uri="/api/hits",
                tag=f"post_new_hit",
                body=payload,
                token=token
            ))

print("ammo.txt успешно сгенерирован")