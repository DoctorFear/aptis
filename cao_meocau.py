#!/usr/bin/env python3
import requests
import os
import time

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"  # giữ nguyên token của bạn

BASE_URL = "https://aptiskey.com/images/meolisteningcau15/meocau{n}.png"
OUT_DIR = "meocau_images"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://aptiskey.com/",
    "Accept": "*/*",
}
COOKIES = {"auth_token": AUTH_TOKEN}

TOTAL = 17
DELAY = 1.0

os.makedirs(OUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

for i in range(1, TOTAL + 1):
    url = BASE_URL.format(n=i)
    filename = f"meocau{i}.png"
    out_path = os.path.join(OUT_DIR, filename)

    if os.path.exists(out_path):
        print(f"⏭️ {filename}: đã có, bỏ qua")
        continue

    try:
        resp = session.get(url, timeout=15)
        ctype = resp.headers.get("content-type", "")

        if resp.status_code == 200 and ctype.startswith("image"):
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print(f"✅ Đã tải {filename} ({len(resp.content)} bytes)")
        else:
            print(f"⚠️ Bỏ qua {filename} (status {resp.status_code}, content-type {ctype})")
    except Exception as e:
        print(f"❌ Lỗi tải {filename}: {e}")

    time.sleep(DELAY)

print("Hoàn tất.")